import ReactEChartsCore from 'echarts-for-react/lib/core';
import * as echarts from 'echarts/core';
import {
  LineChart,
  // BarChart,
  // PieChart,
  // ScatterChart,
  // RadarChart,
  // MapChart,
  // TreeChart,
  // TreemapChart,
  // GraphChart,
  // GaugeChart,
  // FunnelChart,
  // ParallelChart,
  // SankeyChart,
  // BoxplotChart,
  // CandlestickChart,
  // EffectScatterChart,
  // LinesChart,
  // HeatmapChart,
  // PictorialBarChart,
  // ThemeRiverChart,
  // SunburstChart,
  // CustomChart,
} from 'echarts/charts';
import {
  // GridSimpleComponent,
  GridComponent,
  // PolarComponent,
  // RadarComponent,
  // GeoComponent,
  // SingleAxisComponent,
  // ParallelComponent,
  // CalendarComponent,
  // GraphicComponent,
  ToolboxComponent,
  TooltipComponent,
  // AxisPointerComponent,
  // BrushComponent,
  TitleComponent,
  // TimelineComponent,
  // MarkPointComponent,
  // MarkLineComponent,
  // MarkAreaComponent,
  // LegendComponent,
  // LegendScrollComponent,
  LegendPlainComponent,
  DataZoomComponent,
  // DataZoomInsideComponent,
  // DataZoomSliderComponent,
  // VisualMapComponent,
  // VisualMapContinuousComponent,
  // VisualMapPiecewiseComponent,
  // AriaComponent,
  // TransformComponent,
  // DatasetComponent,
} from 'echarts/components';
// Import renderer, note that introducing the CanvasRenderer or SVGRenderer is a required step
import {
  CanvasRenderer,
  // SVGRenderer,
} from 'echarts/renderers';
import {
  CardContent,
} from "@mui/material";

export default function ECharts(props) {
  echarts.use(
    [
      TitleComponent,
      LegendPlainComponent,
      TooltipComponent,
      DataZoomComponent,
      ToolboxComponent,
      GridComponent,
      LineChart,
      CanvasRenderer,
    ]
  );
  return (
    <CardContent>
      <ReactEChartsCore
        echarts={echarts}
        option={{
          title: {
            text: props.title,
          },
          legend: {},
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
          },
          dataZoom: [
            {
              type: 'slider',
              show: true,
              xAxisIndex: [0],
              startValue: 0,
              endValue: 29
            },
            {
              type: 'inside',
              xAxisIndex: [0],
              start: 0,
              end: 29
            }
          ],
          toolbox: {
            show: true,
            feature: {
              dataZoom: {
                show: true
              },
              dataView: { readOnly: true },
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