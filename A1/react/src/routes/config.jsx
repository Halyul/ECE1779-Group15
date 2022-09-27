export default function Config() {
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
  
export const ConfigRoute = {
  name: "Config",
  path: "config"
};