/**
 * StringConcat - Auto-sizing STRING list builder
 *
 * Sử dụng vòng lặp kiểm tra trạng thái cực nhẹ (500ms/lần) để đảm bảo không
 * bao giờ trượt widget của ComfyUI.
 */

import { app } from "../../scripts/app.js";

const NODE_NAME = "StringConcat";
const INPUT_PREFIX = "string_";
const INPUT_TYPE = "STRING";

app.registerExtension({
  name: "sortlist.StringConcat",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;

    // ── onNodeCreated ────────────────────────────────────────────────────────
    const origCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      if (origCreated) origCreated.apply(this, arguments);

      const node = this;
      let lastCount = -1;

      // Dùng một vòng lặp vĩnh viễn siêu nhẹ để theo dõi Widget (do Hook callback 
      // bị vòng luẩn quẩn của ComfyUI chặn).
      node._syncInterval = setInterval(() => {
        if (!node.widgets) return;
        const countWidget = node.widgets.find((w) => w.name === "input_count");
        if (!countWidget) return;

        const val = parseInt(countWidget.value, 10);
        if (!isNaN(val) && val !== lastCount) {
            lastCount = val;

            const currentInputs = node.inputs ? node.inputs.filter((inp) => inp.name.startsWith(INPUT_PREFIX)) : [];
            let changed = false;

            if (currentInputs.length < val) {
                for (let i = currentInputs.length; i < val; i++) {
                    node.addInput(`${INPUT_PREFIX}${i + 1}`, INPUT_TYPE);
                }
                changed = true;
            } else if (currentInputs.length > val) {
                for (let i = currentInputs.length - 1; i >= val; i--) {
                    const idx = node.inputs.findIndex((inp) => inp.name === `${INPUT_PREFIX}${i + 1}`);
                    if (idx !== -1) node.removeInput(idx);
                }
                changed = true;
            }

            if (changed) {
                app.graph.setDirtyCanvas(true, true);
            }
        }
      }, 300); // Quét mỗi 0.3s
    };

    // Dọn dẹp sạch sẽ khi xóa node, tránh chạy chìm
    const origRemoved = nodeType.prototype.onRemoved;
    nodeType.prototype.onRemoved = function () {
        if (this._syncInterval) {
            clearInterval(this._syncInterval);
        }
        if (origRemoved) origRemoved.apply(this, arguments);
    };

    // ── onConfigure ──────────────────────────────────────────────────────────
    const origConfigure = nodeType.prototype.onConfigure;

    nodeType.prototype.onConfigure = function (info) {
      if (origConfigure) origConfigure.apply(this, arguments);
      const node = this;

      setTimeout(() => {
        const countWidget = node.widgets?.find((w) => w.name === "input_count");
        if (countWidget) {
            const currentInputs = (node.inputs || []).filter((inp) => inp.name.startsWith(INPUT_PREFIX)).length;
            if (currentInputs > parseInt(countWidget.value, 10)) {
                countWidget.value = currentInputs;
            }
        }
      }, 500);
    };
  },
});
