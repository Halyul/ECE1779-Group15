export default function Image() {
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
  
export const ImageRoute = {
  name: "Image",
  path: "image"
};

export const ImageWithKeyRoute = {
  name: "Image with Key",
  path: "image/:key"
};