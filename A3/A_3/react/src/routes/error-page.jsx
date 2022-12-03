import {
  useNavigate,
} from "react-router-dom";
import {
  Container,
  Typography,
  Button,
} from "@mui/material";
import { useRouteError } from "react-router-dom";
import { BasicCard } from "@/components/card";

export default function ErrorPage() {
  const error = useRouteError();
  const navigate = useNavigate();
  console.error(error);

  return (
    <Container
      sx={{
        maxWidth: "768px !important",
        width: "90vw",
        height: "inherit",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "stretch",
      }}
    >
      <BasicCard
        title={`${error.status} ${error.data ? error.statusText : ""}`}
        content={
          <Typography variant="body1">
            {error.data ? error.data : error.statusText}
          </Typography>
        }
        actions={
          <Button
            size="small"
            style={{
              marginLeft: "auto",
            }}
            onClick={() => {
              navigate(-1, { replace: true });
            }}
          >
            Back
          </Button>
        }
      />
    </Container>
  );
}