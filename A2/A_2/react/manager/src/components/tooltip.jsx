import {
    Tooltip,
} from "@mui/material";
  
export function TooltipOnError(props) {
    return (
        <Tooltip
            open={props.open}
            onBlur={() => props.handleClose()}
            disableFocusListener
            disableHoverListener
            disableTouchListener
            title={props.title}
        >
            {props.body}
        </Tooltip>
    );
}