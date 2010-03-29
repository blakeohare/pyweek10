using System;
using System.Windows;
using System.Windows.Controls;
using System.Collections.Generic;
using System.Windows.Media.Imaging;
using System.Linq;
using System.Text;

namespace PyWeekMapEditor
{
	public class Tile
	{
		public string Name { get; private set; }
		public string Id { get; private set; }
		public BitmapSource Source { get; private set; }
		public Tile(string[] images, string id, string name) : base()
		{
			this.Id = id;
			this.Name = name;
			if (images.Length > 0 && images[0].Trim().Length > 0)
			{
				string file = MainWindow.TileImagesDirectory + "\\" + images[0].Trim() + ".png";
				this.Source = new System.Windows.Media.Imaging.BitmapImage(new Uri(file));
			}
			else
			{
				this.Source = null;
			}
		}

		public static Image GetImageFromTile(Tile tile, int x, int y)
		{
			Image img = new Image() {
				Width = 16,
				Height = 16,
				Margin = new Thickness(x * 16, y * 16, 0, 0),
				HorizontalAlignment = HorizontalAlignment.Left,
				VerticalAlignment = VerticalAlignment.Top };
			if (tile != null)
			{
				img.Source = tile.Source;
			}

			return img;
		}
	}

}
