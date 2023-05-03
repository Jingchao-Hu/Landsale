import arcpy
import os
import math
import time
# set the main function
def main():
    # set workspace
    arcpy.env.workspace = "\\\VDIDRIVE\\MYHOME\\jhubi\\Desktop\\RA\\cityarea\\"  
    # set the input coordination
    input_point = arcpy.Point(116.412, 40.186) 
    input_shp = "\\\VDIDRIVE\\MYHOME\\jhubi\\Desktop\\RA\\cityarea\\cityborderPCS\\cityborderPCS.shp"  # the original shp data contains the information of city border
    #corresPolygon is the city information contains the input point, we give it a name first
    corresPolygon = "corresPolygon"+str(int(input_point.X * 1000))+"_"+str(int(input_point.Y * 1000))+".shp"
    #name the triangularFacetShp which is the eight triangle layers using input data as the origin
    triangularFacetShp = "triangularFacetPolygon"+str(int(input_point.X * 1000))+"_"+str(int(input_point.Y * 1000))+".shp"
    #name the final eight quadrants shp we want
    finalEightQuadrantsShp = "finalEightQuadrants"+str(int(input_point.X * 1000))+"_"+str(int(input_point.Y * 1000))+".shp"
    
    #execute the function
    city = get_city_info(input_point,input_shp,corresPolygon)
    cutPolylon(input_point,corresPolygon,triangularFacetShp,finalEightQuadrantsShp)
    



# define the function to get the information of corresponding city
def get_city_info(input_point,input_shp,corresPolygon):
    
    # define a spatial reference using WGS84 
    sr = arcpy.SpatialReference(4326)  
    # get the information of input shp
    desc = arcpy.Describe(input_shp)
    # define a spatial reference using input shp
    spatial_ref = desc.spatialReference
    point_projected = arcpy.PointGeometry(input_point, sr).projectAs(spatial_ref)  # change the reference of input data from WGS84 to the one input shp use
    
    #using a cursor to find the city cntain the input point
    city = None
    with arcpy.da.SearchCursor(input_shp, ["FID", "SHAPE@", "OBJECTID", "省代码", "省", "市", "area"]) as cursor:
        for row in cursor:
            if row[1].contains(point_projected):
                city = row
                break
    if city is None:
        print("未找到包含该点的地级市")
    else:
        
        #creat correspolygon shp to save the city information
        arcpy.CreateFeatureclass_management(arcpy.env.workspace,corresPolygon,'Polygon',spatial_reference = spatial_ref)       
        corresPolygonName = os.path.splitext(corresPolygon)[0]        
        arcpy.AddField_management(corresPolygonName, "ProvCode", "LONG")
        arcpy.AddField_management(corresPolygonName, "ProvName", "TEXT")
        arcpy.AddField_management(corresPolygonName, "CityName", "TEXT")
        arcpy.AddField_management(corresPolygonName, "area", "FLOAT")
        
        #use a cursor to put the information from city to correspolygon layer
        rows = arcpy.InsertCursor(corresPolygon)
        
        
        n = 1
        while n<=len(city[1]):
            row = rows.newRow()
            polygon = arcpy.Polygon(city[1][n-1])  
            row.shape = polygon            
            row.ProvCode = city[3]
            row.ProvName = city[4]
            row.CityName = city[5]
            row.area = city[6]
            rows.insertRow(row)
            n = n+1
        del row
        del rows

        return city


    
def cutPolylon(input_point,corresPolygon,triangularFacetShp,finalEightQuadrantsShp):
    # define a spatial reference using WGS84
    sr = arcpy.SpatialReference(4326)  
    # get the information of input shp
    desc = arcpy.Describe(corresPolygon)
    # define a spatial reference using input shp
    spatial_ref = desc.spatialReference
    point_projected = arcpy.PointGeometry(input_point, sr).projectAs(spatial_ref)  # change the reference of input data from WGS84 to the one input shp use
    
    #form eight triangulars base on the input point and two points far away from the origin    
    
    Xori = point_projected[0].X
    Yori = point_projected[0].Y
    
    array1, array2,array3,array4,array5,array6,array7,array8,= (arcpy.Array() for i in range(8))
    for i in range(8):
        if i==0: 
            #first quadrant
            array1.add(point_projected[0])
            point1 = arcpy.Point(Xori,Yori+1000000) #large enough to cover any city
            array1.add(point1)
            X2 = Xori + 1000000*math.cos(45*math.pi/180)*math.sin(45*math.pi/180)
            Y2 = Yori + 1000000*math.cos(45*math.pi/180)*math.cos(45*math.pi/180)
            point2 = arcpy.Point(X2,Y2)
            array1.add(point2)
        if i==1: 
            array2.add(point_projected[0])
            point1 = arcpy.Point(Xori+1000000, Yori) 
            array2.add(point1)
            array2.add(point2)
        if i==2: 
            array3.add(point_projected[0])
            point1 = arcpy.Point(Xori+1000000, Yori) 
            array3.add(point1)
            X2 = Xori + 1000000*math.cos(45*math.pi/180)*math.cos(45*math.pi/180)
            Y2 = Yori - 1000000*math.cos(45*math.pi/180)*math.sin(45*math.pi/180)
            point2 = arcpy.Point(X2,Y2)
            array3.add(point2)
        if i==3: 
            array4.add(point_projected[0])
            point1 = arcpy.Point(Xori,Yori-1000000) 
            array4.add(point1)
            array4.add(point2)
        if i==4: 
            
            array5.add(point_projected[0])
            point1 = arcpy.Point(Xori,Yori-1000000) 
            array5.add(point1)
            X2 = Xori - 1000000*math.cos(45*math.pi/180)*math.sin(45*math.pi/180)
            Y2 = Yori - 1000000*math.cos(45*math.pi/180)*math.cos(45*math.pi/180)
            point2 = arcpy.Point(X2,Y2)
            array5.add(point2)
        if i==5: 
            array6.add(point_projected[0])
            point1 = arcpy.Point(Xori-1000000,Yori) 
            array6.add(point1)
            array6.add(point2)
        if i==6: 
            array7.add(point_projected[0])
            point1 = arcpy.Point(Xori-1000000,Yori) 
            array7.add(point1)
            X2 = Xori - 1000000*math.cos(45*math.pi/180)*math.cos(45*math.pi/180)
            Y2 = Yori + 1000000*math.cos(45*math.pi/180)*math.sin(45*math.pi/180)
            point2 = arcpy.Point(X2,Y2)
            array7.add(point2)
        if i==7: 
            array8.add(point_projected[0])
            point1 = arcpy.Point(Xori,Yori+1000000) 
            array8.add(point1)
            array8.add(point2)
        #finish making the points of eight triangles
    
    #put eight triangles in the same layer
    polygonGeometryList = []
    #creat eight polygons using three points
    for i in range(8):
        polygon = arcpy.Polygon(eval('array'+str(i+1))).projectAs(spatial_ref)
        polygonGeometryList.append(polygon)
        eval('array'+str(i+1)).removeAll()
        
    # save the eight triangles to triangularfacetshp
    arcpy.CopyFeatures_management(polygonGeometryList, triangularFacetShp)
    triangularFacetShpName = os.path.splitext(triangularFacetShp)[0]
    arcpy.AddField_management(triangularFacetShpName, "Area", "DOUBLE")
    # calculate area
    expression = "!SHAPE.area@SQUAREKILOMETERS!"
    arcpy.CalculateField_management(triangularFacetShpName, "Area", expression, "PYTHON_9.3")
    
    #intersect the correspolygon with triangularfacetshp get the result 
    corresShpName = os.path.splitext(corresPolygon)[0]
    finalEightQuadrantsShpName = os.path.splitext(finalEightQuadrantsShp)[0]
    arcpy.Intersect_analysis([triangularFacetShpName,corresShpName],finalEightQuadrantsShpName,'ALL',"","")
    
    arcpy.AddField_management(finalEightQuadrantsShpName, "ReArea_km2", "DOUBLE")
    # calculate area
    expression = "!SHAPE.area@SQUAREKILOMETERS!"
    arcpy.CalculateField_management(finalEightQuadrantsShpName, "ReArea_km2", expression, "PYTHON_9.3")
            

if __name__ == "__main__":
    main()