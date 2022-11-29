import {
  Form,
} from "react-router-dom";
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

export function FormCard(props) {
  return (
    <Card sx={{ marginBottom: "1rem" , ...props.sx}}>
      <Form
        id={props.id}
        method={props.method}
        onSubmit={props.onSubmit}
      >
        <CardHeader
        title={props.title}
        subheader={props.subtitle}
        action={props.header_action}
      />
        <CardContent>
          {props.content}
        </CardContent>
        {props.actions && (
        <CardActions disableSpacing>
          {props.actions}
          </CardActions>
        )}
      </Form>
    </Card>
  );
}