import {
  Form,
} from "react-router-dom";
import {
  Card,
  CardHeader,
  CardActions,
  CardContent,
  Button,
  IconButton,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";

export function BasicCard(props) {
  return (
    <Card sx={{ marginBottom: "1rem" }}>
      <CardHeader title={props.title} />
      <CardContent>{props.body}</CardContent>
      {props.actions && (
        <CardActions>
          {props.actions.map((action) => (
            <Button key={action.label} size="small" onClick={action.onClick}>
              {action.content}
            </Button>
          ))}
        </CardActions>
      )}
    </Card>
  );
}

export function RefreshCard(props) {
  return (
    <Card sx={{ marginBottom: "1rem" }}>
      <Form method="POST" id="image-form">
        <CardHeader
          action={
            <IconButton
              aria-label="refresh"
              type="submit"
              onClick={props.handleOnClick}
            >
              <RefreshIcon />
            </IconButton>
          }
          title={props.title}
          subheader={props.subtitle}
        />
      </Form>
      <CardContent>{props.body}</CardContent>
    </Card>
  );
}
