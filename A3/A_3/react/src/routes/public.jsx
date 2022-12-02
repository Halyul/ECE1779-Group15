import { useState, useEffect } from "react";
import {
  Navigate,
    useLocation,
    useLoaderData,
  useActionData,
  NavLink
} from "react-router-dom";
import {
  Box,
  Button,
  TextField,
  Grid,
} from "@mui/material";
import { useSelector, useDispatch } from 'react-redux'
import { TooltipOnError } from "@/components/tooltip";
import SubmissionPrompt from "@/components/submission-prompt";

export default function Public() {
  const actionResponse = useActionData();

  const [submitted, setSubmitted] = useState(false);

  return (
    <>
      
      <SubmissionPrompt
        failed={{
          title: "Failed to commit changes",
          text: actionResponse?.statusText,
        }}
        submitting={{
          text: "Commiting changes...",
          open: submitted,
          setOpen: setSubmitted,
        }}
        submittedText="Changes committed successfully"
        submissionStatus={actionResponse}
      />
    </>
  );
}

export const PublicRoute = {
    name: "Public",
    path: "public",
};
  
export const PublicWithShareKeyRoute = {
    name: "Public with Share Key",
    path: "public/:shareKey",
  };
