#
#  MapWindowDelegate.py
#  Maprender
#
#  Created by Daniel Sabo on 4/24/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

from Foundation import *
import pgdb as DBAPI
import mapnik

class MapWindowDelegate(NSObject):
    mapView   = objc.IBOutlet()
    mapWindow = objc.IBOutlet()
    
    mapCenterLat = objc.ivar()
    mapCenterLon = objc.ivar()
    mapZoom      = objc.ivar()
    
    def init(self):
        self = super(self.__class__, self).init()
        if self is None:
            return None
        
        self.mapCenterLat = 0.0
        self.mapCenterLon = 0.0
        self.mapZoom = 100
        
        return self
    
    def awakeFromNib(self):
        self.db_args = None
        self.mapView.setCenter_([self.mapCenterLat, self.mapCenterLon])
        self.mapView.setZoom_(self.mapZoom)
    
    def setDBParams(self,dbParams):
        #FIXME: This should be replaced by preferences
        self.db_args = dbParams
    
    def loadMap_(self, mapName):
        con = DBAPI.connect(**self.db_args)
        try:
            table = mapName + "_polygon"
            cur = con.cursor()
            cur.execute("select proj4text from spatial_ref_sys where srid=Find_SRID('public', '%s','way')" % table)
            proj4 = cur.fetchall()[0][0]
            #FIXME: This needs to use the mapnik projection not the DB one...
            prj = mapnik.Projection(str(proj4))
            cur.execute("select ST_XMin(st_estimated_extent),ST_YMin(st_estimated_extent),ST_XMax(st_estimated_extent),ST_YMax(st_estimated_extent) from ST_Estimated_Extent('%s','way');" % table)
            bounds = cur.fetchall()[0]
            size = [bounds[2] - bounds[0], bounds[3] - bounds[1]]
            center = [size[0] + bounds[0], size[1] + bounds[1]]
            center_ll = prj.inverse(mapnik.Coord(center[0], center[1]))
            self.mapCenterLat = center_ll.x
            self.mapCenterLon = center_ll.y
            self.mapView.setCenter_([self.mapCenterLat, self.mapCenterLon])
        finally:
            con.close()
        
        #FIXME: Calculate Zoom
            
        self.mapWindow.makeKeyAndOrderFront_(self)
    
    @objc.IBAction
    def updateMap_(self, sender):
        self.mapView.setCenter_([float(self.mapCenterLat), float(self.mapCenterLon)])
        self.mapView.setZoom_(self.mapZoom)
        self.mapView.setNeedsDisplay_(True)
