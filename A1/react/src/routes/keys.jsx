import {
  useLoaderData,
  NavLink
} from "react-router-dom";
import {
  Card,
  CardHeader,
  CardContent,
  List,
  ListItem,
  ListItemText,
  IconButton,

} from "@mui/material";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import RefreshIcon from '@mui/icons-material/Refresh';

export async function loader({ params }) {
  // const image = await getImage(params.imageKey);
  // return image;
  return ["123", "456", "789", "101112"];
}

export default function Keys() {
  const keys = useLoaderData();
  return (
    <Card sx={{ marginBottom: "1rem" }}>
      <CardHeader
        action={
          <IconButton
            aria-label="refresh"
            onClick={() => {
        
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        title="Existing Keys"
      />
      <CardContent>
        <List>
          {keys.map((key) => (
            <ListItem
              key={key}
              secondaryAction={
                <NavLink to={`../image/${key}`}>
                  <IconButton
                    edge="end"
                    aria-label={`Go to image with key ${key}`}
                  >
                    <NavigateNextIcon />
                  </IconButton>
                </NavLink>
              }
            >
              <ListItemText primary={key} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}

export const KeysRoute = {
  name: "Keys",
  path: "keys",
};
