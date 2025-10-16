import express from "express";
import bodyParser from "body-parser";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import multer from "multer";
import fs from "fs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const port = 3000;

//Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(join(__dirname, "public"))); 

//Routes
app.get("/", (req, res) => {
  res.sendFile(join(__dirname, "public", "index.html"));
});

app.get("/login", (req, res) => {
  res.sendFile(join(__dirname, "pages", "login.html"));
});

app.get("/notes", (req, res) => {
  res.sendFile(join(__dirname, "pages", "notes.html"));
});

app.get("/resume", (req, res) => {
  res.sendFile(join(__dirname, "templates", "index.html"));
});

app.get("/notes_upload", (req, res) => {
  res.sendFile(join(__dirname, "pages", "notes_upload.html"));
});

// Set up multer for file uploads

const uploadDir = join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir); // save files in /uploads folder
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + "-" + file.originalname);
  }
});

const upload = multer({ storage });

app.use(express.static(join(__dirname, "public")));

app.post("/upload", upload.single("noteFile"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  res.send(`
    <div style="font-family: sans-serif; text-align: center; margin-top: 100px;">
      <h2 style="color: limegreen;">✅ File Uploaded Successfully!</h2>
      <p>Saved as: <b>${req.file.filename}</b></p>
      <a href="/" style="color: #007bff; text-decoration: none;">Go Back</a>
    </div>
  `);
});

//login form submission handling
app.post("/submit", (req, res) => {
  const { username, password } = req.body;
  res.send(`Username: ${username}, Password: ${password}`);
});

app.listen(port, () => {
  console.log(`✅ Server running at http://localhost:${port}`);
});
