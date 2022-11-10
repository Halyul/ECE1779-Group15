import ReactEcharts from "echarts-for-react";
import {
  CardContent,
} from "@mui/material";

export default function ECharts(props) {
  return (
    <CardContent>
      <ReactEcharts
        option={{
          title: {
            text: props.title,
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          dataZoom: [
            {
              type: 'slider',
              show: true,
              startValue: 0,
              endValue: 29
            },
          ],
          toolbox: {
            show: true,
            feature: {
              dataView: { readOnly: true },
              magicType: { type: props.magicTypes },
              saveAsImage: {}
            }
          },
          xAxis: props.xAxis,
          yAxis: props.yAxis,
          series: props.series
        }}
      />
    </CardContent>
  )
}