document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) {
    alert("Please upload an image!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.error) {
      document.getElementById("result").textContent = `Error: ${data.error}`;
    } else {
      document.getElementById("result").textContent = `Prediction: ${data.label}`;
    }
  } catch (error) {
    document.getElementById("result").textContent = `Error: ${error.message}`;
  }
});
