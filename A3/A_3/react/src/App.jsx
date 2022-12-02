import React from 'react';
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from "react-router-dom";
import { StyledEngineProvider } from '@mui/material/styles';
import Root from "@/routes/root";
import ErrorPage from "@/routes/error-page";
import Login, {
  LoginRoute,
} from "@/routes/login";
import Register, {
  RegisterRoute,
  action as registerAction,
} from "@/routes/register";
import Index, {
  IndexRoute
} from "@/routes/user/index";
import Upload, {
  UploadRoute,
  action as uploadAction,
} from "@/routes/user/upload";
import Image, {
  ImageRoute,
  PublicRoute,
  PublicWithShareKeyRoute,
  loader as imageLoader,
  action as imageAction,
  publicAction as publicAction,
} from "@/routes/image";
import Album, {
  AlbumRoute,
  loader as albumLoader,
  action as albumAction,
} from "@/routes/user/album";
import Protected from '@/components/protected';
import store, { persistor } from '@/libs/store';
import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/integration/react'
import 'reset-css';
import '@/App.css';
import Config from "../config";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <Root
          title={Config.appName}
          destinations={[
            IndexRoute,
            UploadRoute,
            AlbumRoute,
          ]}
        />
      }
      errorElement={<ErrorPage />}
    >
      <Route errorElement={<ErrorPage />}>
      <Route
          path={PublicRoute.path}
          element={
            <Image
              route={PublicRoute.path}
            />
          }
          action={publicAction}
        />
      <Route
          path={PublicWithShareKeyRoute.path}
          element={
            <Image
              route={PublicWithShareKeyRoute.path}
            />
          }
          loader={imageLoader}
          action={publicAction}
        />
      <Route
          path={LoginRoute.path}
          element={<Login />}
        />
        <Route
          path={RegisterRoute.path}
          element={<Register />}
          action={registerAction}
        />
        <Route index element={
          <Protected
            permission="all"
            destination="/public"
          >
            <Index />
          </Protected>
        } />
        <Route
          path={UploadRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Upload />
            </Protected>
          }
          action={uploadAction}
        />
        <Route
          path={ImageRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Image 
                route={ImageRoute.path}
              />
            </Protected>
          }
          loader={imageLoader}
          action={imageAction}
        />
        <Route
          path={AlbumRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Album />
            </Protected>
          }
          loader={albumLoader}
          action={albumAction}
        />
      </Route>
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <StyledEngineProvider injectFirst>
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
            <RouterProvider router={router} />
        </PersistGate>
      </Provider>
    </StyledEngineProvider>
  </React.StrictMode>
)