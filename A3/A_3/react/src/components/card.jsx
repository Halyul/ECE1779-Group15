import {
  Form,
} from "react-router-dom";
import {
  Card,
  CardMedia,
  CardHeader,
  CardActions,
  CardContent,
} from "@mui/material";

export function BasicCard(props) {
  return (
    <Card sx={{ marginBottom: "1rem", ...props.sx }}>
      {props.image && (
        <CardMedia component="img" image={props.image.content} alt={props.image.key} />
      )}
        {(props.title || props.subheader || props.header_action) && (
          <CardHeader
            title={props.title}
            subheader={props.subheader}
            action={props.header_action}
          />
        )}
        {props.content && (
          <CardContent>{props.content}</CardContent>
        )}
        {props.actions && (
          <CardActions disableSpacing>
            {props.actions}
          </CardActions>
        )}
    </Card>
  );
}

export function FormCard(props) {
  return (
    <Card sx={{ marginBottom: "1rem", ...props.sx }}>
      {props.image && (
        <CardMedia component="img" image={props.image.content} alt={props.image.key} />
      )}
      <Form
        id={props.id}
        method={props.method}
        onSubmit={props.onSubmit}
      >
        {(props.title || props.subheader || props.header_action) && (
          <CardHeader
            title={props.title}
            subheader={props.subheader}
            action={props.header_action}
          />
        )}
        {props.content && (
          <CardContent>{props.content}</CardContent>
        )}
        {props.actions && (
          <CardActions disableSpacing>
            {props.actions}
          </CardActions>
        )}
      </Form>
    </Card>
  );
}