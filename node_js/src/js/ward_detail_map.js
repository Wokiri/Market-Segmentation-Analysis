import 'ol/ol.css'
import GeoJSON from 'ol/format/GeoJSON'
import VectorSource from 'ol/source/Vector'
import { Circle as CircleStyle, Style, Fill, Text, Stroke } from 'ol/style'
import VectorLayer from 'ol/layer/Vector'
import { Map, View } from 'ol'
import sync from 'ol-hashed'
import {
  Attribution,
  defaults as defaultControls,
  ZoomSlider,
} from 'ol/control'
import TileLayer from "ol/layer/Tile";
import XYZ from "ol/source/XYZ";

const OpenStreetMapLayer = new TileLayer({
    title: "OpenStreetMap",
    type: "base",
    opacity: OpenStreetMap_Opacity,
  
    source: new XYZ({
      attributions: "Open Street map ",
      url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    }),
  });


const ward_detail_div = document.getElementById('ward_detail_map')

// Customers source
const CustomerVector = new VectorSource({
    features: new GeoJSON().readFeatures(ward_customers_geojson, {
      dataProjection: 'EPSG:4326',
      featureProjection: 'EPSG:3857',
      extractGeometryName: true,
    }),
  })

  
// Customer visual style
const CustomerTextLabel = feature => feature.get('customer_name')

const CustomerTextStyle = feature => {
  return new Text({
    textAlign: 'center',
    textBaseline: 'middle',
    font: `11px "Open Sans", "Arial Unicode MS", "sans-serif"`,
    text: CustomerTextLabel(feature),
    placement: 'point',
  })
}

// Styling Customer
const CustomerPointStyle = feature => {
  return new Style({
    image: new CircleStyle({
      radius: 4,
      fill: new Fill({ color: 'rgb(255, 255, 255)' }),
      //   stroke: new Stroke({ color: 'rgb(255, 255, 255)', width: 4 }),
      text: CustomerTextStyle(feature),
    }),
  })
}

// Customer layer
const CustomerLayer = new VectorLayer({
  source: CustomerVector,
  style: CustomerPointStyle,
})

// Wards source
const WardsVector = new VectorSource({
  features: new GeoJSON().readFeatures(ward_geojson, {
    dataProjection: 'EPSG:4326',
    featureProjection: 'EPSG:3857',
    extractGeometryName: true,
  }),
})

const WardTextLabel = feature => `${feature.get('ward')} Ward`

const WardTextStyle = feature =>
  new Text({
    textAlign: 'center',
    textBaseline: 'middle',
    font: `bold 20px system-ui`,
    text: WardTextLabel(feature),
    placement: 'polygon',
    fill: new Fill({
      color: '#331100',
    }),
  })

// Styling Ward
const WardPolygonStyle = feature => {
  return new Style({
    fill: new Fill({
      color: 'rgba(51, 17, 0, 0.2)',
    }),
    stroke: new Stroke({
      color: '#662200',
      width: 4,
    }),
    text: WardTextStyle(feature),
  })
}

// Ward layer
const WardLayer = new VectorLayer({
  source: WardsVector,
  style: WardPolygonStyle,
})


let expandedAttribution = new Attribution({
  collapsible: false,
})

const ward_detail_map = new Map({
  controls: defaultControls({ attribution: false }).extend([
    expandedAttribution,
    new ZoomSlider(),
  ]),
  target: ward_detail_div,
  layers: [OpenStreetMapLayer, WardLayer, CustomerLayer],
  view: new View({
    maxZoom: 28,
    minZoom: 1,
  }),
})

sync(ward_detail_map)

const mapExtent = WardLayer.getSource().getExtent()
ward_detail_map.getView().fit(mapExtent, ward_detail_map.getSize())

let checkSize = () => {
  let isLess600 = ward_detail_map.getSize()[0] < 600
  expandedAttribution.setCollapsible(isLess600)
  expandedAttribution.setCollapsed(isLess600)
}
checkSize()
window.addEventListener('resize', checkSize)


let attributionComplete = false;
ward_detail_map.on("rendercomplete", function (evt) {
  if (!attributionComplete) {
    let attribution = document.getElementsByClassName("ol-attribution")[0];
    let attributionList = attribution.getElementsByTagName("ul")[0];
    let firstLayerAttribution = attributionList.getElementsByTagName("li")[0];
    let olAttribution = document.createElement("li");
    olAttribution.innerHTML =
      '<a href="https://openlayers.org/" class="font-barlow-light">OpenLayers Docs</a> &#x2503; ';
    attributionList.insertBefore(olAttribution, firstLayerAttribution);
    attributionComplete = true;
  }
});