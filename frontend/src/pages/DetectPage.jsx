import React, { useState, useRef } from "react";
import {
  Box, CircularProgress, Alert, Typography, Paper,
  Chip, Table, TableBody, TableCell, TableHead,
  TableRow, LinearProgress, Divider,
} from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { detectFaces } from "../services/faceApi";

export default function DetectPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileRef = useRef();

  const handleFile = async (file) => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const r = await detectFaces(fd);
      setResult(r.data);
    } catch (e) {
      setError(e.response?.data?.detail || "Detection failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      {/* Drop zone */}
      <Paper
        variant="outlined"
        onClick={() => fileRef.current.click()}
        onDrop={(e) => { e.preventDefault(); handleFile(e.dataTransfer.files[0]); }}
        onDragOver={(e) => e.preventDefault()}
        sx={{
          p: 3, mb: 2, textAlign: "center", cursor: "pointer", borderStyle: "dashed",
          "&:hover": { bgcolor: "action.hover" },
        }}
      >
        <input ref={fileRef} type="file" hidden accept=".jpg,.jpeg,.png,.bmp,.webp"
          onChange={(e) => handleFile(e.target.files[0])} />
        {loading
          ? <Box>
              <CircularProgress size={28} sx={{ mb: 1 }} />
              <Typography color="text.secondary">Detecting faces…</Typography>
            </Box>
          : <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 1 }}>
              <UploadFileIcon color="action" />
              <Typography color="text.secondary">
                Drag & drop or click — JPG / PNG / BMP / WEBP
              </Typography>
            </Box>
        }
      </Paper>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {result && (
        <Box>
          {/* Stats bar */}
          <Box sx={{ display: "flex", gap: 1.5, mb: 2, flexWrap: "wrap" }}>
            <Chip
              label={`${result.face_count} face${result.face_count !== 1 ? "s" : ""} detected`}
              color={result.face_count > 0 ? "success" : "default"}
              size="medium"
            />
            <Chip label={`${result.image_width} × ${result.image_height} px`}
              variant="outlined" size="small" />
          </Box>

          {/* Annotated image */}
          <Paper variant="outlined" sx={{ p: 1, mb: 2, textAlign: "center" }}>
            <img
              src={`data:image/jpeg;base64,${result.annotated_image}`}
              alt="annotated"
              style={{ maxWidth: "100%", maxHeight: 480, borderRadius: 4 }}
            />
          </Paper>

          {/* Face details table */}
          {result.faces.length > 0 && (
            <>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="subtitle2" gutterBottom>Face Details</Typography>
              <Paper variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow sx={{ bgcolor: "grey.50" }}>
                      <TableCell>#</TableCell>
                      <TableCell>Position (x, y)</TableCell>
                      <TableCell>Size (w × h)</TableCell>
                      <TableCell>Confidence</TableCell>
                      <TableCell sx={{ minWidth: 120 }}>Bar</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {result.faces.map((f, i) => (
                      <TableRow key={i} hover>
                        <TableCell>{i + 1}</TableCell>
                        <TableCell>({f.x}, {f.y})</TableCell>
                        <TableCell>{f.width} × {f.height}</TableCell>
                        <TableCell>
                          <Chip label={`${f.confidence}%`}
                            color={f.confidence >= 90 ? "success" : f.confidence >= 70 ? "warning" : "error"}
                            size="small" />
                        </TableCell>
                        <TableCell>
                          <LinearProgress variant="determinate" value={f.confidence}
                            color={f.confidence >= 90 ? "success" : f.confidence >= 70 ? "warning" : "error"}
                            sx={{ height: 6, borderRadius: 3 }} />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Paper>
            </>
          )}

          {result.face_count === 0 && (
            <Alert severity="info">No faces detected. Try a clearer image with visible faces.</Alert>
          )}
        </Box>
      )}
    </Box>
  );
}
