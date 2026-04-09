/**
 * StringConcat - Auto-sizing STRING list builder
 *
 * Đồng bộ số slot thông qua giá trị `input_count`, siêu tối ưu.
 */

import { app } from "../../scripts/app.js";

const NODE_NAME = "StringConcat";
const INPUT_PREFIX = "string_";
const INPUT_TYPE = "STRING";

function syncInputsWithCount(node, count) {
  count = parseInt(count, 10);
  if (isNaN(count)) return;

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

function hookWidget(node) {
  if (node._widgetHooked) return true;

  const countWidget = node.widgets?.find((w) => w.name === "input_count");
  if (!countWidget) return false;

  const origCallback = countWidget.callback;
  countWidget.callback = function (val) {
    if (origCallback) origCallback.apply(this, arguments);

    if (node._timeout) clearTimeout(node._timeout);
    node._timeout = setTimeout(() => {
        syncInputsWithCount(node, val);
    }, 30);
  };

  node._widgetHooked = true;
  return true;
}

app.registerExtension({
  name: "sortlist.StringConcat",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;

    // ── onNodeCreated ────────────────────────────────────────────────────────
    const origCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      if (origCreated) origCreated.apply(this, arguments);
      const node = this;

      // ComfyUI có thể sinh widget sau onNodeCreated một nhịp, nên ta quét tìm nó.
      let attempts = 0;
      const tryHook = () => {
        if (hookWidget(node)) {
          // Bắt được widget rồi thì tạo dây cắm ngay lập tức:
          if (!app.configuringGraph) {
            const countWidget = node.widgets?.find((w) => w.name === "input_count");
            if (countWidget) syncInputsWithCount(node, countWidget.value);
          }
        } else if (attempts < 10) {
          attempts++;
          setTimeout(tryHook, 50);
        }
      };
      tryHook();
    };

    // ── onConfigure ──────────────────────────────────────────────────────────
    const origConfigure = nodeType.prototype.onConfigure;

    nodeType.prototype.onConfigure = function (info) {
      if (origConfigure) origConfigure.apply(this, arguments);
      const node = this;

      let attempts = 0;
      const tryHookConfig = () => {
        if (hookWidget(node)) {
            const countWidget = node.widgets?.find((w) => w.name === "input_count");
            if (countWidget) {
                const currentInputs = (node.inputs || []).filter((inp) => inp.name.startsWith(INPUT_PREFIX)).length;
                if (currentInputs > countWidget.value) {
                    countWidget.value = currentInputs;
                }
                syncInputsWithCount(node, countWidget.value);
            }
        } else if (attempts < 10) {
            attempts++;
            setTimeout(tryHookConfig, 50);
        }
      };
      tryHookConfig();
    };
  },
});
