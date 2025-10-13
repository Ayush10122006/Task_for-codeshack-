import express from "express";
import bodyParser from "body-parser";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

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
  res.sendFile(join(__dirname, "pages", "resume.html"));
});

//login form submission handling
app.post("/submit", (req, res) => {
  const { username, password } = req.body;
  res.send(`Username: ${username}, Password: ${password}`);
});

app.listen(port, () => {
  console.log(`✅ Server running at http://localhost:${port}`);
});
