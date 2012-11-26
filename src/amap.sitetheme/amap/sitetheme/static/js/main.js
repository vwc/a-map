/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false, window:false, location:false */
/*globals jQuery, portal_url, Modernizr, alert, history, window, location*/

(function ($) {
    $(document).ready(function () {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) {
            // it's not realistic to think we can deal with all the bugs
            // of IE 6 and lower. Fortunately, all this is just progressive
            // enhancement.
            return;
        }
        $('div[data-appui="venuemap"]').each(function () {
            var target_id = $(this).data('appui-target');
            var mapdata_url = $(this).data('appui-source');
            $.getJSON(mapdata_url, function (item) {
                //coords = item.geometry.coordinates;
                //props = item.properties;
                var features = item.features;
                var m = mapbox.map(target_id);
                m.addLayer(mapbox.layer().id('vwerbung.map-f3yuziyn'));
                var markerLayer = mapbox.markers.layer().features(features);
                var interaction = mapbox.markers.interaction(markerLayer);
                m.addLayer(markerLayer).setExtent(markerLayer.extent());
                interaction.formatter(function(feature) {
                    var o = '<h3><a target="_blank" href="' + feature.properties.url + '">' + feature.properties.title + '</a></h3>' +
                        '<p>' + feature.properties.decription + '</p>';
                    return o;
                });
                m.ui.zoomer.add();
                m.ui.zoombox.add();
                m.centerzoom({
                    lat: features[0].geometry.coordinates[1],
                    lon: features[0].geometry.coordinates[0]
                }, 11);
            });
        });
    });
}(jQuery));
