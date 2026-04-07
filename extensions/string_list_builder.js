/**
 * StringListBuilder - Auto-expanding dynamic STRING inputs
 *
 * Khi nối dây vào slot cuối cùng → tự thêm slot mới
 * Khi ngắt dây → dọn slot rỗng ở cuối (giữ lại ít nhất 1)
 */

import { app } from "../../scripts/app.js";

const NODE_NAME = "StringListBuilder";
const INPUT_PREFIX = "string_";
const INPUT_TYPE = "STRING";

/**
 * Lấy danh sách index của các string_N inputs
 */
function getStringInputIndices(node) {
  return node.inputs
    .map((inp, idx) => ({ inp, idx }))
    .filter(({ inp }) => inp.name.startsWith(INPUT_PREFIX));
}

/**
 * Thêm slot string mới vào cuối
 */
function addStringInput(node) {
  const count = getStringInputIndices(node).length;
  node.addInput(`${INPUT_PREFIX}${count + 1}`, INPUT_TYPE);
  node.setDirtyCanvas(true, true);
}

/**
 * Xóa slot rỗng ở cuối, giữ lại ít nhất `minKeep` slots
 */
function pruneTrailingEmpty(node, minKeep = 1) {
  const stringSlots = getStringInputIndices(node);
  // Đếm bao nhiêu slot rỗng liên tiếp từ cuối
  let toRemove = 0;
  for (let i = stringSlots.length - 1; i >= 0; i--) {
    const { inp } = stringSlots[i];
    if (!inp.link) {
      toRemove++;
    } else {
      break;
    }
  }

  // Giữ lại ít nhất `minKeep` slot rỗng (để luôn có chỗ nối)
  const removeCount = Math.max(0, toRemove - minKeep);
  for (let r = 0; r < removeCount; r++) {
    // Luôn xóa slot cuối cùng
    node.removeInput(node.inputs.length - 1);
  }

  if (removeCount > 0) {
    node.setDirtyCanvas(true, true);
  }
}

app.registerExtension({
  name: "sortlist.StringListBuilder",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;

    // ── onConnectionsChange ──────────────────────────────────────────────────
    const origConnectionsChange = nodeType.prototype.onConnectionsChange;

    nodeType.prototype.onConnectionsChange = function (
      type,
      slotIndex,
      connected,
      linkInfo
    ) {
      if (origConnectionsChange) {
        origConnectionsChange.apply(this, arguments);
      }

      // Chỉ quan tâm INPUT side
      if (type !== LiteGraph.INPUT) return;

      const stringSlots = getStringInputIndices(this);
      if (stringSlots.length === 0) return;

      const lastSlot = stringSlots[stringSlots.length - 1];

      if (connected && slotIndex === lastSlot.idx) {
        // Nối vào slot cuối → thêm slot mới
        addStringInput(this);
      } else if (!connected) {
        // Ngắt kết nối → dọn slot rỗng cuối (giữ 1 slot trống)
        pruneTrailingEmpty(this, 1);
        // Đánh số lại tên các slot
        renumberInputs(this);
      }
    };

    // ── onNodeCreated ────────────────────────────────────────────────────────
    const origCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      if (origCreated) origCreated.apply(this, arguments);
      // Đảm bảo luôn có ít nhất 1 slot khi tạo mới
      if (getStringInputIndices(this).length === 0) {
        addStringInput(this);
      }
    };
  },
});

/**
 * Đánh số lại các slot sau khi xóa để tên luôn liên tục: string_1, string_2, ...
 */
function renumberInputs(node) {
  let counter = 1;
  for (const inp of node.inputs) {
    if (inp.name.startsWith(INPUT_PREFIX)) {
      inp.name = `${INPUT_PREFIX}${counter}`;
      counter++;
    }
  }
  node.setDirtyCanvas(true, true);
}
