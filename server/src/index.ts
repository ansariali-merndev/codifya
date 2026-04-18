import express from "express";
import type { Express, Request, Response } from "express";

const app: Express = express();
const PORT = 5000;

app.get("/", (req: Request, res: Response) => {
  console.log(req);
  res.json({
    success: true,
    message: "Welcome to the codiya server",
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
