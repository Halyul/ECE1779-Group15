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
  const body = [];

  if (props.title || props.subheader || props.header_action) {
    body.push(
      <CardHeader
        title={props.title}
        subheader={props.subheader}
        action={props.header_action}
        key="header"
      />
    );
  }

  if (props.content) {
    body.push(
      <CardContent
        key="content"
      >
        {props.content}
      </CardContent>
    );
  }

  if (props.actions) {
    body.push(
      <CardActions
        disableSpacing
        key="actions"
      >
        {props.actions}
      </CardActions>
    );
  }

  return (
    <Card sx={{ margin: "1rem auto", maxWidth: "768px", ...props.sx }}>
      {props.image && (
        <CardMedia component="img" image={props.image} />
      )}
      {props.media && (
        <CardMedia>
          {props.media}
        </CardMedia>
      )}
      {props.subcomponent ? (
        <props.subcomponent.el {...props.subcomponent.props}>
          {body}
        </props.subcomponent.el>
      ) : body}
    </Card>
  );
}

export function FormCard(props) {
  return (
    <BasicCard
      {...props}
      subcomponent={{
        el: Form,
        props: {
          id: props.id,
          method: props.method,
          encType: props.encType,
          onSubmit: props.onSubmit,
        },
      }}
    />
  );
}