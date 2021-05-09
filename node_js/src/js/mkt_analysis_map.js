import 'ol/ol.css'
import GeoJSON from 'ol/format/GeoJSON'
import VectorSource from 'ol/source/Vector'
import { Circle as CircleStyle, Style, Fill, Text, Stroke } from 'ol/style'
import VectorLayer from 'ol/layer/Vector'
import { Map, View } from 'ol'
import Select from 'ol/interaction/Select'
import Overlay from 'ol/Overlay'
import sync from 'ol-hashed'
import {
  Attribution,
  defaults as defaultControls,
  ZoomSlider,
} from 'ol/control'

// const customers_geojson = require('./customers.json')
// const market_wards_geojson = require('./market_wards.json')

const mkt_div = document.getElementById('mkt_map')
const mkt_popup = document.getElementById('mkt_popup')
const mkt_PopupContent = document.getElementById('mkt_PopupContent')
const mkt_popupcloser = document.getElementById('mkt_popupcloser')

// Customers source
const CustomerVector = new VectorSource({
  features: new GeoJSON().readFeatures(customers_geojson, {
    dataProjection: 'EPSG:4326',
    featureProjection: 'EPSG:3857',
    extractGeometryName: true,
  }),
})

// Customer visual style
const CustomerTextLabel = feature => `${feature.get('customer_name')}`

const CustomerTextStyle = feature => {
  return new Text({
    textAlign: 'center',
    textBaseline: 'middle',
    font: `18px Helvetica, sans-serif`,
    text: CustomerTextLabel(feature),
    placement: 'polygon',
    fill: new Fill({
      color: 'rgb(0, 0, 0)',
    }),
  })
}

// Styling Customer
const CustomerPointStyle = feature => {
  return new Style({
    image: new CircleStyle({
      radius: 2.5,
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
  features: new GeoJSON().readFeatures(market_wards_geojson, {
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
    font: `14px Helvetica, sans-serif`,
    text: WardTextLabel(feature),
    placement: 'polygon',
    fill: new Fill({
      color: '#99ccff',
    }),
  })

// Styling Ward
const WardPolygonStyle = feature => {
  return new Style({
    fill: new Fill({
      color: '#331100',
    }),
    stroke: new Stroke({
      color: '#99ccff',
      width: 0.75,
    }),
    text: WardTextStyle(feature),
  })
}

// Ward layer
const WardLayer = new VectorLayer({
  source: WardsVector,
  style: WardPolygonStyle,
})

const theOverlay = new Overlay({
  element: mkt_popup,
  autoPan: true,
  autoPanAnimation: {
    duration: 250,
  },
})

mkt_popupcloser.onclick = () => {
  theOverlay.setPosition(undefined)
  mkt_popupcloser.blur()
  return false
}

let expandedAttribution = new Attribution({
  collapsible: false,
})

const mkt_map = new Map({
  controls: defaultControls({ attribution: false }).extend([
    expandedAttribution,
    new ZoomSlider(),
  ]),
  target: mkt_div,
  layers: [WardLayer, CustomerLayer],
  overlays: [theOverlay],
  view: new View({
    maxZoom: 28,
    minZoom: 1,
  }),
})

sync(mkt_map)

const mapExtent = WardLayer.getSource().getExtent()
mkt_map.getView().fit(mapExtent, mkt_map.getSize())

let checkSize = () => {
  let isLess600 = mkt_map.getSize()[0] < 600
  expandedAttribution.setCollapsible(isLess600)
  expandedAttribution.setCollapsed(isLess600)
}
checkSize()
window.addEventListener('resize', checkSize)

// If Ward is selected get feature info, don't otherwise
const populate_PopupContent = theFeature => {
  mkt_PopupContent.style.padding = '5px'
  mkt_PopupContent.innerHTML = `
      <p class='font-barlow-light fs-6 m-0'>SubCounty: <span class='font-barlow-semibold'>${theFeature.sub_county}</span></p>
      <p class='font-barlow-light fs-6 m-0'>Ward: <span class='font-barlow-semibold'>${theFeature.ward}</span></p>
      <a class="btn btn-outline-info mt-2" href='/mkt-detail/${theFeature.pk}'>Market Details</a>
      `
}

// sampleAnnotations selection option
const singleMapClick = new Select({
  layers: [WardLayer],
})

mkt_map.addInteraction(singleMapClick)

let selected = null
mkt_map.on('singleclick', evt => {
  mkt_map.forEachFeatureAtPixel(evt.pixel, layer => {
    selected = layer
  })

  if (selected) {
    let click_coords = evt.coordinate
    theOverlay.setPosition(click_coords)
    console.log(selected.getProperties())
    populate_PopupContent(selected.getProperties())
    selected = null
  } else {
    theOverlay.setPosition(undefined)
    mkt_popupcloser.blur()
  }
})
