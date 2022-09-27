import { BasicCard } from "../components/card.jsx";

export default function Index() {
  return (
      <BasicCard
        title="Welcome"
        body="Please select a destination from the menu."
      />
  );
}

export const IndexRoute = {
  name: "Home",
  path: "",
};
