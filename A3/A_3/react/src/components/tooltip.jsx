import {
  Tooltip as MuiTooltip
} from "@mui/material";

export function TooltipOnError(props) {
  return (
    <MuiTooltip
      open={props.open}
      onBlur={() => props.handleClose()}
      disableFocusListener
      disableHoverListener
      disableTouchListener
      title={props.title}
    >
      {props.body}
    </MuiTooltip>
  );
}

export function Tooltip(props) {
  return (
    <MuiTooltip
      title={props.title}
    >
      {props.body}
    </MuiTooltip>
  );
}