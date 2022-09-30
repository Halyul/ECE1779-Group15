import {
  useNavigate,
} from "react-router-dom";
import {
  Container,
  Typography,
} from "@mui/material";
import { useRouteError } from "react-router-dom";
import { BasicCard } from "../components/card";

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
        title={`${error.status} ${error.data ? (error.statusText || error.statusText) : ""}`}
        body={
          <Typography variant="body1">
            {error.data ? error.data : (error.statusText || error.statusText)}
          </Typography>
        }
        actions={[
          {
            label: "Go back",
            content: "Go back",
            onClick: () => {
              navigate(-1);
            }
          }
        ]}
      />
    </Container>
  );
}