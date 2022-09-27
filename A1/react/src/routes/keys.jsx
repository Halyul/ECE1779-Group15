export default function Keys() {
    return (
      <p id="zero-state">
        This is a demo for React Router.
        <br />
        Check out{" "}
        <a href="https://reactrouter.com/">
          the docs at reactrouter.com
        </a>
        .
      </p>
    );
}
  
export const KeysRoute = {
  name: "Keys",
  path: "keys"
};