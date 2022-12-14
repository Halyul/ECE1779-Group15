import {
  Box,
} from "@mui/material";
import {
  DataGrid,
  GridToolbar,
} from '@mui/x-data-grid';
import {
  BasicCard
} from "@/components/card";

export default function DataTable(props) {
  return (
    <>
      <BasicCard
        title={props.title}
        header_action={props.header_action}
        content={
          props.rows.length > 0 ? (
            <Box sx={{ height: "61.8vh", maxHeight: 768 }}>
              <DataGrid
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
              />
            </Box>
          ) : (
            <Typography variant="body1">No data found.</Typography>
          )
        }
        sx={{
          maxWidth: "unset",
        }}
      />
      {props.children}
    </>
  )
}