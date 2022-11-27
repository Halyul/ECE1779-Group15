import React from 'react';
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from "react-router-dom";
import { StyledEngineProvider } from '@mui/material/styles';
import Root from "./routes/root";
import ErrorPage from "./routes/error-page";
import Index, {
  IndexRoute
} from "./routes/index";
import Upload, {
  UploadRoute,
  action as uploadAction,
} from "./routes/upload";
import Image, {
  ImageRoute,
  loader as imageLoader,
  action as imageAction,
} from "./routes/image";
import Keys, {
  KeysRoute,
  loader as keysLoader,
  action as keysAction,
} from "./routes/keys";
import 'reset-css';
import './App.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <Root
          title="User UI"
          destinations={[
            IndexRoute,
            UploadRoute,
            KeysRoute,
          ]}
        />
      }
      errorElement={<ErrorPage />}
    >
      <Route errorElement={<ErrorPage />}>
        <Route index element={<Index />} />
        <Route
          path={UploadRoute.path}
          element={<Upload />}
          action={uploadAction}
        />
        <Route
          path={ImageRoute.path}
          element={<Image />}
          loader={imageLoader}
          action={imageAction}
        />
        <Route
          path={KeysRoute.path}
          element={<Keys />}
          loader={keysLoader}
          action={keysAction}
        />
      </Route>
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <StyledEngineProvider injectFirst>
        <RouterProvider router={router} />
    </StyledEngineProvider>
  </React.StrictMode>
)