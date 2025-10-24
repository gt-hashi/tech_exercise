const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const downloadLink = document.getElementById("downloadLink");
const convertBtn = document.getElementById("convertBtn");


// 選択中のファイルを保持する変数を追加
let selectedFile = null;

// handleFile の最後で選択ファイルを記録
function handleFile(file) {
  selectedFile = file;   // ★ 追加
  const reader = new FileReader();
  reader.onload = e => {
    preview.innerHTML = `<img src="${e.target.result}" alt="preview" />`;
    downloadLink.style.display = "inline-block";
    downloadLink.href = e.target.result;
    downloadLink.download = file.name.replace(/\.[^.]+$/, '') + "_nostalgic.jpg";
  };
  reader.readAsDataURL(file);
}

// クリックでファイル選択
dropArea.addEventListener("click", () => fileInput.click());

// ドラッグオーバー時の見た目
["dragenter", "dragover"].forEach(evt => {
  dropArea.addEventListener(evt, e => {
    e.preventDefault(); e.stopPropagation();
    dropArea.classList.add("dragover");
  });
});
["dragleave", "drop"].forEach(evt => {
  dropArea.addEventListener(evt, e => {
    e.preventDefault(); e.stopPropagation();
    dropArea.classList.remove("dragover");
  });
});

// ドロップされたファイルを処理
dropArea.addEventListener("drop", e => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

// ファイル選択時
fileInput.addEventListener("change", e => {
  const file = e.target.files[0];
  if (file) handleFile(file);
});

// 変換ボタン（サーバーに送信）
convertBtn.addEventListener("click", () => {
  if (!selectedFile) {
    alert("Please select your images");
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile);

  // ★ 処理中メッセージを表示
  statusMsg.textContent = "Processing.....";


  fetch("/process_image/", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.url) {
      // サーバーから返ってきた変換済み画像を表示
      preview.innerHTML = `<img src="${data.url}" alt="converted" />`;
      downloadLink.style.display = "inline-block";
      downloadLink.href = data.url;
      downloadLink.download = "converted.jpg";

      // 履歴リストに追加
      const historyList = document.getElementById("history-list");

      // ★ ここで空メッセージを削除
      const emptyMsg = document.getElementById("empty-msg");
      if (emptyMsg) emptyMsg.remove();

      // aタグを作成してダウンロード属性を付与
      const linkElem = document.createElement("a");
      linkElem.href = data.url;
      linkElem.download = data.name || "converted.jpg"; // サーバーからファイル名を返しているなら data.name を使う
      linkElem.title = "クリックでダウンロード";

      // サムネイル画像を作成して a に入れる
      const imgElem = document.createElement("img");
      imgElem.src = data.url;
      imgElem.alt = "generated image";
      imgElem.width = 120;

      linkElem.appendChild(imgElem);

      // 履歴リストの先頭に追加
      historyList.prepend(linkElem);

      // ★ 完了メッセージに切り替え
      statusMsg.textContent = "Done!";


    } else {
      alert("Fail to process.");
    }
  })
  .catch(err => {
    console.error(err);
    alert("Failed connecting server.");
  });
});