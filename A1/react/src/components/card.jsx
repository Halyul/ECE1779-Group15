import {
  Card,
  CardHeader,
  CardActions,
  CardContent,
  Button,
} from "@mui/material";

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
