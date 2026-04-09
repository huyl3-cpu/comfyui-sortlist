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
  if (!node.inputs) return [];
  return node.inputs
    .map((inp, idx) => ({ inp, idx }))
    .filter(({ inp }) => inp.name.startsWith(INPUT_PREFIX));
}

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
}

/**
 * Cập nhật động số lượng input slots (chống lag bằng cách xử lý gộp)
 */
function updateStringInputs(node) {
  const stringSlots = getStringInputIndices(node);
  if (stringSlots.length === 0) {
    node.addInput(`${INPUT_PREFIX}1`, INPUT_TYPE);
    node.setDirtyCanvas(true, true);
    return;
  }

  // Tìm số slot rỗng trống ở cuối cùng
  let emptyCount = 0;
  for (let i = stringSlots.length - 1; i >= 0; i--) {
    if (!stringSlots[i].inp.link) {
      emptyCount++;
    } else {
      break;
    }
  }

  let changed = false;

  // Luôn đảm bảo có CHÍNH XÁC 1 slot rỗng cuối cùng
  if (emptyCount === 0) {
    node.addInput(`${INPUT_PREFIX}${stringSlots.length + 1}`, INPUT_TYPE);
    changed = true;
  } else if (emptyCount > 1) {
    const slotsToRemove = emptyCount - 1;
    for (let r = 0; r < slotsToRemove; r++) {
      const currentSlots = getStringInputIndices(node);
      const lastSlotIdx = currentSlots[currentSlots.length - 1].idx;
      node.removeInput(lastSlotIdx);
    }
    changed = true;
  }

  if (changed) {
    renumberInputs(node);
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

      // === TỐI ƯU HÓA: Bỏ qua khi đang load workflow (chống đơ máy) ===
      if (app.configuringGraph) {
        return;
      }

      // === TỐI ƯU HÓA: Sử dụng Debounce để gom thao tác ===
      if (!this._dynamicSchedule) {
        this._dynamicSchedule = setTimeout(() => {
          this._dynamicSchedule = null;
          updateStringInputs(this);
        }, 50);
      }
    };

    // ── onNodeCreated ────────────────────────────────────────────────────────
    const origCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      if (origCreated) origCreated.apply(this, arguments);
      
      // Không tự thêm input nếu như đang load file JSON
      if (app.configuringGraph) return;

      updateStringInputs(this);
    };
    
    // ── onConfigure ──────────────────────────────────────────────────────────
    // Chạy một lần update sau khi workflow tải xong (đảm bảo hiển thị đúng)
    const origConfigure = nodeType.prototype.onConfigure;
    
    nodeType.prototype.onConfigure = function (info) {
      if (origConfigure) origConfigure.apply(this, arguments);
      // LiteGraph có thể chưa kết nối dây ngay lúc onConfigure, dùng setTimeout nhẹ
      setTimeout(() => {
         updateStringInputs(this);
      }, 100);
    };
  },
});
