import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";
import FaceIcon from "@mui/icons-material/Face";

export default function Header() {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <FaceIcon sx={{ mr: 1 }} />
        <Typography variant="h6" fontWeight="bold">
          Face Detection System
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
