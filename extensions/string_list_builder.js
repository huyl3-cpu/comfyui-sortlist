/**
 * StringListBuilder - Auto-sizing STRING list builder
 *
 * Chỉ đồng bộ số slot thông qua giá trị `input_count`, hoàn toàn loại bỏ lag!
 */

import { app } from "../../scripts/app.js";

const NODE_NAME = "StringListBuilder";
const INPUT_PREFIX = "string_";
const INPUT_TYPE = "STRING";

function syncInputsWithCount(node, count) {
  const currentInputs = node.inputs ? node.inputs.filter((inp) => inp.name.startsWith(INPUT_PREFIX)) : [];

  let changed = false;
  // Thêm slot nếu đang thiếu
  if (currentInputs.length < count) {
    for (let i = currentInputs.length; i < count; i++) {
      node.addInput(`${INPUT_PREFIX}${i + 1}`, INPUT_TYPE);
    }
    changed = true;
  }
  // Xóa bớt slot từ dưới lên nếu dư
  else if (currentInputs.length > count) {
    for (let i = currentInputs.length - 1; i >= count; i--) {
      const idx = node.inputs.findIndex((inp) => inp.name === `${INPUT_PREFIX}${i + 1}`);
      if (idx !== -1) node.removeInput(idx);
    }
    changed = true;
  }

  if (changed) {
    node.setDirtyCanvas(true, true);
  }
}

app.registerExtension({
  name: "sortlist.StringListBuilder",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;

    // Loại bỏ hoàn toàn onConnectionsChange do widget đã đảm nhiệm việc đó!

    // ── onNodeCreated ────────────────────────────────────────────────────────
    const origCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      if (origCreated) origCreated.apply(this, arguments);

      const node = this;
      const countWidget = node.widgets?.find((w) => w.name === "input_count");

      if (countWidget) {
        const origCallback = countWidget.callback;
        countWidget.callback = function (val) {
          if (origCallback) origCallback.apply(this, arguments);

          // Tránh spam cập nhật liên tục nếu user kéo/giữ chuột
          if (node._timeout) clearTimeout(node._timeout);
          node._timeout = setTimeout(() => {
            syncInputsWithCount(node, val);
          }, 30);
        };

        // Nếu mới thả node ra lần đầu, cập nhật số lượng slot ngay
        if (!app.configuringGraph) {
          syncInputsWithCount(node, countWidget.value);
        }
      }
    };

    // ── onConfigure (Dành cho load workflow cũ/mới) ──────────────────────────
    const origConfigure = nodeType.prototype.onConfigure;

    nodeType.prototype.onConfigure = function (info) {
      if (origConfigure) origConfigure.apply(this, arguments);

      const node = this;
      const countWidget = node.widgets?.find((w) => w.name === "input_count");

      if (countWidget) {
        const currentInputs = (node.inputs || []).filter((inp) => inp.name.startsWith(INPUT_PREFIX)).length;

        // Cơ chế Migration:
        // Nếu load từ workflow phiên bản cũ (lúc chưa có input_count nhưng đang có 5 dây string)
        // -> Giá trị countWidget.value sẽ bị default = 2 và sẽ lỡ xóa mất dây của khách.
        // Giải pháp: Ép input_count phải tối thiểu bằng số dây đang có!
        if (currentInputs > countWidget.value) {
          countWidget.value = currentInputs;
        }

        setTimeout(() => {
          syncInputsWithCount(node, countWidget.value);
        }, 50);
      }
    };
  },
});
