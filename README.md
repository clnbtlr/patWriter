# patWriter

patWriter is a Python script that converts any lines drawn in AutoCAD into a hatch pattern file (.pat) for use in AutoCAD.

Although AutoCAD includes a standard library of hatch patterns, custom hatches allow you to create and use your own patterns to suit your needs. The advantage of hatch patterns over AutoCAD's SuperHatch tool is that hatches support annotative scaling which automatically resizes the pattern based on the current viewport or annotation scale while SuperHatch does not.

The examples in this repository are designed for use with Tailte Éireann (formerly Ordnance Survey Ireland) mapping applications.

<img width="992" height="426" alt="patWriter hatch pattern" src="https://github.com/user-attachments/assets/a5e42b22-0029-41e4-951b-d2ce8ecec31d" />

This code is based on the [pat_writer](https://github.com/Justin-Yeung/pat_writer) repository by Justin-Yeung which is mainly intended for Rhino 8.

## Usage

1. In AutoCAD, draw one unit cell of the pattern you want to use as hatch pattern. Polylines, Arcs, Splines, etc. should be exploded and divided into individual line objects.
2. Using AutoCAD's Data Extraction wizard, export information related to the unit cell line objects:
   1. The first time you extract data, you are prompted to save the data extraction settings in a data extraction (.dxex) file. This file can also be used again as a template to perform the same type of extraction in a different drawing.
   2. Select the line objects in the current drawing using the selection tool.
   3. On the next page, ensure only line objects are selected in the table.
   4. In the properties table, include <code>Angle</code>, <code>End X</code>, <code>End Y</code>, <code>Length</code>, <code>Start X</code> and <code>Start Y</code> from the Geometry category.
   5. Refine the data table if required.
   6. Output the data to an external <code>.txt</code> file.
   7. Create the file by clicking Finish.
3. After downloading the [patWriter.py](https://github.com/clnbtlr/patWriter/blob/main/patWriter.py) script, run it using:
   ```
   python3 patWriter.py -f <path_to_txt_data_extraction> -b bbx bby -w <hatch_name>
   ```
   replacing <code><path_to_txt_data_extraction></code> to the location of the .txt file exported from  AutoCAD's Data Extraction wizard in the previous step, <code>bbx bby</code> with bounding box length and width of the unit cell and <code><hatch_name></code> with the name for writing the .pat file.
5. To make the hatch pattern available for use in AutoCAD, add its location as a custom folder to the application support files search paths in Options > Files > Support File Search Path > Add.

## Examples

| Name | Pattern |
| ------------- | ------------- |
| Woodland Coniferous | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/40a28978-2a90-496e-9142-c5adeb7c62de" />  |
| Woodland Deciduous  | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/8a7c870c-72eb-4496-80d5-bd7d3ca9c8a5" />  |
| Woodland Mixed      | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/1e093782-4e1f-4042-a506-866c6f378436" />  |
| Outcrop             | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/4387e0ff-90f6-4395-a19b-af10e5cbe205" />  |
| Marsh               | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/84dfc317-84b7-439d-bc31-b945dea1d593" />  |
| Bog                 | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/b6b96b42-e939-4506-b2cb-4654946a3c91" />  |
| Flatrock            | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/53ed30d7-bdd7-4469-9f7a-49ed49042d1c" />  |
| Sand                | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/2f804d21-c577-46a3-a510-a2f066ec8fda" />  |
| Sand and Shingle    | <img width="64" height="64" alt="image" src="https://github.com/user-attachments/assets/038abb9d-8607-4897-9b1e-68a989055c5b" />  |
