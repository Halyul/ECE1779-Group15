import { useEffect } from "react";
import {
  useLocation,
  useOutletContext,
} from "react-router-dom";
import {
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Box,
  Divider
} from "@mui/material";
import { red, blue } from "@mui/material/colors";
import { BasicCard } from "@/components/card.jsx";

const members = [
  {
    color: red[500],
    name: "Teng Shu",
    responsibility: "Backend Developer",
  },
  {
    color: blue[500],
    name: "Haoyu Xu",
    responsibility: "Frontend Developer",
  },
  {
    color: red[500],
    name: "Xiaoyu Zhai",
    responsibility: "Backend Developer",
  },
];

export default function Index() {
  const location = useLocation();
  const [bubble, setBubble] = useOutletContext();

  useEffect(() => {
    if (location.state?.isLoggedIn) {
      setBubble({
        ...bubble,
        snackbar: {
          open: true,
          message: "You are now logged in!"
        }
      })
    }
  }, [location])

  return (
    <>
      <BasicCard
        title="Welcome"
        content={
          <Typography variant="body1">
            Please select a destination from the menu.
          </Typography>
        }
      />
      <BasicCard
      title="Members"
      content={
        <List sx={{ width: "100%", bgcolor: "background.paper" }}>
          {members.map((member) => (
            <Box key={member.name}>
              <ListItem alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: member.color }}>
                    {member.name
                      .split(" ")
                      .map((name) => name[0])
                      .join("")}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={member.name}
                  secondary={
                    <Typography
                      sx={{ display: "inline" }}
                      component="div"
                      variant="body2"
                      color="text.primary"
                    >
                      {member.responsibility}
                    </Typography>
                  }
                />
              </ListItem>
              <Divider variant="inset" component="li" />
            </Box>
          ))}
        </List>
      }
    />
    </>
  );
}

export const IndexRoute = {
  name: "Home",
  path: "",
};
