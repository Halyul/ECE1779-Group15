import {
  useState,
  useEffect
} from "react";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Snackbar,
} from "@mui/material";
import DOMPurify from 'dompurify';

export default function SubmissionPrompt(props) {
  const [submitionSuccess, setSubmitionSuccess] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    if (props.submissionStatus) {
      props.submitting.setOpen(false);
      if (props.submissionStatus.status !== 200) {
        setDialogOpen(true);
      } else {
        setSubmitionSuccess(true);
      }
    }
  }, [props.submissionStatus]);

  const handleDialogClose = () => {
    setDialogOpen(false);
  };
  const handleSnackbarSuccessClose = () => {
    setSubmitionSuccess(false);
  };

  return (
    <>
      <Dialog
        open={dialogOpen}
        onClose={handleDialogClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{props.failed.title}</DialogTitle>
        <DialogContent>
          <DialogContentText
            id="alert-dialog-description"
            dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(props.failed.text) }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Close</Button>
        </DialogActions>
      </Dialog>
      <Snackbar open={props.submitting.open} message={props.submitting.text} />
      <Snackbar
        open={submitionSuccess}
        message={props.submittedText}
        autoHideDuration={6000}
        onClose={handleSnackbarSuccessClose}
      />
    </>
  );
}
