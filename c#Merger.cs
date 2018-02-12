//Create a new object of PdfDoument, insert a page
PdfDocument doc = new PdfDocument();
PdfPageBase page = doc.Pages.Add(PdfPageSize.A4, new PdfMargins());
//Set font, brush
PdfFont font = new PdfFont(PdfFontFamily.TimesRoman, 12f, PdfFontStyle.Bold);
PdfBrush brush = PdfBrushes.Black;
float x = 50;
float y = 50;
float tempX = 0;
//Draw sting in Pdf
string text = "Phone Number: ";
page.Canvas.DrawString(text, font, brush, x, y);
//Insert textbox
tempX = font.MeasureString(text).Width + x + 15;
PdfTextBoxField textbox = new PdfTextBoxField(page, "TextBox");
textbox.Bounds = new RectangleF(tempX, y, 100, 15);
textbox.BorderWidth = 0.75f;
textbox.BorderStyle = PdfBorderStyle.Solid;doc.Form.Fields.Add(textbox);
//Add a tooltip to textbox
doc.Form.Fields["TextBox"].ToolTip = "Please insert a valid phone Number";
doc.SaveToFile("sample.pdf", FileFormat.PDF); 