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
import { retrieveKeys } from "../libs/api";

export async function loader({ params }) {
  const keys = await retrieveKeys();
  if (keys.status_code !== 200) {
    throw new Response(keys.data.message, {
      status: keys.status_code,
      statusText: "",
    });
  }
  return keys.data;
}

export default function Keys() {
  const loaderResponse = useLoaderData();
  const [keyList, setKeyList] = useState(loaderResponse.keys);
  return (
    <Card sx={{ marginBottom: "1rem" }}>
      <CardHeader
        action={
          <IconButton
            aria-label="refresh"
            onClick={() => {
              const keys = retrieveKeys();
              if (keys.status_code !== 200) {
                // TODO: handle error
              }
              setKeyList(keys.data.keys);
            }}
          >
            <RefreshIcon />
          </IconButton>
        }
        title="Existing Keys"
      />
      <CardContent>
        <List>
          {keyList.map((key) => (
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
