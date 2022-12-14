import { useState } from "react";
import { styled } from '@mui/material/styles';
import {
  Box,
  Collapse,
  IconButton,
} from "@mui/material";
import {
  DataGrid,
  GridToolbar,
} from '@mui/x-data-grid';
import { BasicCard } from "@/components/card";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

export default function DataTable(props) {
  const [expanded, setExpanded] = useState(true);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <>
      <BasicCard
        title={props.title}
        header_action={
          <>
            {props.header_action}
            <ExpandMore
              expand={expanded}
              onClick={handleExpandClick}
              aria-expanded={expanded}
            >
              <ExpandMoreIcon />
            </ExpandMore>
          </>
        }
        content={
          <>
            <Collapse in={expanded} timeout="auto" unmountOnExit>
            <Box sx={{ height: "61.8vh", maxHeight: 768 }}>
              <DataGrid
                initialState={props.initialState}
                getRowId={props.getRowId}
                rows={props.rows}
                columns={props.columns}
                loading={props.isRefreshing}
                selectionModel={props.selectionModel}
                onSelectionModelChange={props.onSelectionModelChange}
                components={{ Toolbar: GridToolbar }}
                componentsProps={{
                  toolbar: {
                    showQuickFilter: true,
                    quickFilterProps: { debounceMs: 500 },
                  },
                }}
                checkboxSelection={props.checkboxSelection}
              />
            </Box>
          </Collapse>
          {props.content}
          </>
        }
        actions={props.actions}
        sx={props.sx}
      />
    </>
  )
}