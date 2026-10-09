import argparse
import pandas as pd
from fractions import Fraction
import numpy as np
import csv

"""
Python script for creating custom hatch patterns (.pat) files for AutoCAD

Hatch pattern file parameters:
{angle},{line.start.x},{line.start.y},{displacement_along_line},{displacement_perpen_line},{length},{dash}

Usage:
python3 patWriter.py -f <path_to_txt_data_extraction> -b bbx bby -w <hatch_name>

"""


def intersect_point_line(pt, line_p1, theta, hyp):
    """
    Python adapted reproduction of mathutils.geometry.intersect_point_line
    
    Parameters:
    pt, line_p1: array-like coordinates [x,y]
    theta: angle of line w.r.t positive x-axis
    hyp: length of line

    Returns:
    closest_point: np.ndarray (coordinates of the projection)
    factor: float (scalar projection distance ali)
    """
    pt = np.asarray(pt)
    line_p1 = np.asarray(line_p1)
    line_p2 = [line_p1[0]+hyp*np.cos(np.radians(theta)),line_p1[1]+hyp*np.sin(np.radians(theta))] # calculate line endpoint from angle and hypotenuse
    line_vec = line_p2 - line_p1 # line direction vector
    pt_vec = pt - line_p1 # point direction vector
    line_len_sq = np.dot(line_vec, line_vec) # squared length of the line segement
    if line_len_sq < 1e-10: # handle the edge case where pt is on line segment
        print(True)
        return line_p1.copy(), 0.0
    factor = np.abs(np.dot(pt_vec, line_vec)/line_len_sq) # scalar factor projection
    closest_point = line_p1 + (line_vec*factor) # closest coordinates on the line
    return closest_point, float(factor)

def main(fn,bb,w):
    df = pd.read_csv(fn,sep='\t',header=0) # Read in data from txt file created using AutoCAD DATAEXTRACTION command
    print(df.to_string())
    lines = []
    for line in range(len(df.index)): # iterates through each line in hatch pattern
        print(line)
        theta = df.Angle[line] # line angle
        length = df.Length[line] # line length
        if round(theta) == 0 or round(theta) == 360: # horizontal line (left to right)
            x0 = df['Start X'][line] # starting x coord of line
            y0 = df['Start Y'][line] # starting y coord of line
            dash = length - bb[0]
            lines.append([round(theta),x0,y0,bb[0],bb[1],length,dash])
        elif round(theta) == 90: # vertical line (bottom to top)
            x0 = df['Start X'][line] # starting x coord of line
            y0 = df['Start Y'][line] # starting y coord of line
            dash = length - bb[1]
            lines.append([round(theta),x0,y0,bb[1],bb[0],length,dash])
        elif round(theta) == 180: # horizontal line (right to left)
            x0 = df['End X'][line] # flips starting x coord of line
            y0 = df['End Y'][line] # flips starting y coord of line
            theta -= 180
            dash = length - bb[0]
            lines[line].append([round(theta),x0,y0,bb[0],bb[1],length,dash])
        elif round(theta) == 270: # vertical line (top to bottom)
            x0 = df['End X'][line] # flips starting x coord of line
            y0 = df['End Y'][line] # flips starting y coord of line
            theta -= 180
            dash = length - bb[1]
            lines.append([round(theta),x0,y0,bb[1],bb[0],length,dash])
        else: # slanted line
            if df['Start X'][line] > df['End X'][line]:
                x0 = df['End X'][line] # flips starting x coord of line
                y0 = df['End Y'][line] # flips starting y coord of line
                if theta > 180 and theta < 270:
                    theta -= 180
            else:
                x0 = df['Start X'][line]
                y0 = df['Start Y'][line]

            tangent = np.tan(np.radians(theta))
            ratio = Fraction(round(tangent*bb[0]/bb[1],2)).limit_denominator()
            m,n = ratio.numerator, ratio.denominator  # calculates approx. interger triangle
            hyp = np.sqrt(m*m*bb[1]*bb[1]+n*n*bb[0]*bb[0]) # hypoteneuse of interger triangle
            atheta = np.degrees(np.arctan2((m*bb[1]),(n*bb[0]))) # approx. angle

            # find next closest point to line
            closestpt = None
            close_dist = np.sqrt(bb[1]*bb[1]+bb[0]*bb[0]) # initalise close_dist
            for i in range(abs(n)):
                for j in range(abs(m)):
                    if not(i==0 and j==0):
                        if theta < 90:
                            pt = [x0+i*bb[0],y0+j*bb[1]]
                        else:
                            pt = [x0+i*bb[0], y0-j*bb[1]]
                        distance = abs((y0-pt[1])*np.cos(np.radians(atheta))-(x0-pt[0])*np.sin(np.radians(atheta))) # distance from point to line defined by point and angle

                        if distance < close_dist: # find closest point to line
                            closestpt = pt
                            close_dist = distance #deltaY
            if closestpt == None:
                #deltaY = 0
                if theta > 0:
                    closestpt = [x0+bb[0],y0+bb[1]]
                else:
                    closestpt = [x0+bb[0],y0-bb[1]]
            #else:
                #deltaY = close_dist

            projpt,factor = intersect_point_line(closestpt, [x0,y0], atheta, hyp) # finds the closest point on the line, and the distance along the line
            if closestpt[1] < round(projpt[1],4):
                deltaX  = hyp - hyp*factor
            else:
                deltaX = hyp*factor
            deltaY = close_dist
            ##### there is still a strange edge case when theta = -45 deg
            #if line == 35:
            #    print(closestpt, [x0,y0], atheta, hyp, projpt,factor,deltaX,deltaY)
            
            lines.append([atheta,x0,y0,deltaX,deltaY,length,length-hyp])

            
    if w != "":
        print(lines)
        with open('.\\'+w.upper()+'.pat', "w") as patfile:
            patfile.write('*'+w.upper()+',\n')
            writer = csv.writer(patfile)
            writer.writerows(lines)
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="Input .txt file created from AutoCAD DATAEXTRACTION")
    parser.add_argument("-b", nargs=2, type=float, required=True, help="Bounding Box (Bx By) of hatch pattern")
    parser.add_argument("-w", type=str, required=False, help="Input name of .pat file")
    args = parser.parse_args()
    main(fn=args.f, bb=args.b, w=args.w)