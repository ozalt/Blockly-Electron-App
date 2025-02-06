const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const fs = require('fs')

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })
  win.loadFile('index.html')
}

// Handle request from renderer to execute Python
ipcMain.on('run-python', (event) => {
  const scriptPath = path.join(__dirname, 'backend.py')
  console.log("Executing Python script:", scriptPath)

  const pythonProcess = spawn('python', [scriptPath])

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python Output: ${data}`)
    event.sender.send('python-output', data.toString())
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`)
    event.sender.send('python-error', data.toString())
  })

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`)
    event.sender.send('python-exit', code)
  })
})


ipcMain.on('save-csv', (event, csvContent) => {
  console.log("Received save-csv event with data:\n", csvContent);  // Debugging

  const dirPath = path.join(__dirname, 'csv_output');
  const filePath = path.join(dirPath, 'blocks.csv');

  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath);
  }

  fs.writeFile(filePath, csvContent, (err) => {
    if (err) {
      console.error("Error saving CSV:", err.message);
      event.sender.send('save-csv-result', 'Error saving CSV: ' + err.message);
    } else {
      console.log("CSV saved successfully.");
      event.sender.send('save-csv-result', 'CSV saved successfully');
    }
  });
});


app.whenReady().then(createWindow)
