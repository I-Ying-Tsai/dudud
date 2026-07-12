# Academic Decompiler (學術論文反組譯器)

基於非線性閉環校驗與多目標產物導出的前沿學術論文編譯優化核心。本專案旨在將隨機的 LLM 語意機率約束於確定性的實體代碼執行沙盒中，徹底斬斷錯誤級聯，並自動還原出最小可行性實作 (MVI) 與技術規格白皮書。

---

## 開發環境與依賴庫宣告 (Prerequisites & Dependencies)

專案採用核心解耦設計，目前基於 **Python 3.12+** 虛擬環境建置。系統運作所需的剛性依賴元件如下：

### 1. 大模型認知算子面 (Cognitive Layer)
* **`google-genai`**
    * **職責**：對接 2026 最新官方 Google GenAI SDK 核心。
    * **用途**：驅動 Frontend 進行大脈絡 PDF 地毯式掃描，以及 Middle-End 的高階邏輯程式碼合成。

### 2. 剛性資料合約與組態 (Data Contract & Config)
* **`pydantic`**
    * **職責**：架構強型別數據合約防火牆。
    * **用途**：強制约束大模型輸出結構，反序列化提煉為中介表示式（Academic IR），不允許任何欄位幻覺。
* **`pydantic-settings`**
    * **職責**：全域環境組態管理。
    * **用途**：收攏系統安全性、模型路由選型及作業系統級別的沙盒動態超時（Timeout）參數。

### 3. 分散式容錯與控制面 (Control Plane Infrastructure)
* **`tenacity`**
    * **職責**：具備隨機抖動（Jitter）的指數退避重試引擎。
    * **用途**：外掛於 API 算子頭上，專職在後台平滑消化雲端基礎設施的 `503 Unavailable` 或 `429 Rate Limit` 等暫時性隨機抖動。

### 4. 實體沙盒運行期 (Deterministic Sandbox Runtime)
* **`numpy`**
    * **職責**：高性能科學計算與矩陣代數核心環境。
    * **用途**：部署於獨立隔離的 Subprocess 子進程沙盒中，作為驗證論文公式矩陣相乘、軸向轉置與數值健康度（防範 NaN/Inf 爆炸）的**客觀物理真理基準（Ground Truth）**。

---
