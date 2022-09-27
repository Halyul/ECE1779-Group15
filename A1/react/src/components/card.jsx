import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

export function BasicCard(props) {
  return (
    <Card>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {props.title}
        </Typography>
        <Typography variant="body1">{props.body}</Typography>
      </CardContent>
    </Card>
  );
}

export function FormCard(props) {
  return (
    <Card>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {props.title}
        </Typography>
        <Typography variant="body1">{props.body}</Typography>
      </CardContent>
    </Card>
  );
}

export function FileCard(props) {

}

export function ImageCard(props) {

}

export function ListCard(props) {
    
}