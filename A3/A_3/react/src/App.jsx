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
  loader as imageLoader,
} from "@/routes/image";
import Photos, {
  PhotosRoute,
  loader as photosLoader,
  action as photosAction,
} from "@/routes/user/photos";
import Share, {
  ShareRoute,
  loader as shareLoader,
  action as shareAction,
} from "@/routes/user/share";
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
            PhotosRoute,
            ShareRoute,
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
          loader={imageLoader}
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
            destination="/login"
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
        />
        <Route
          path={PhotosRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Photos />
            </Protected>
          }
          loader={photosLoader}
          action={photosAction}
        />
        <Route
          path={ShareRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Share />
            </Protected>
          }
          loader={shareLoader}
          action={shareAction}
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