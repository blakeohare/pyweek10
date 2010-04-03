using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.IO;

namespace PyWeekMapEditor
{
	public class Map
	{
		private string file = null;
		private Tile[] front;
		private Tile[] middle;
		private Tile[] back;

		private Dictionary<string, string> values = new Dictionary<string, string>();

		private int width;
		private int height;

		public Map(int width, int height)
		{
			this.width = width;
			this.height = height;
			front = new Tile[width * height];
			middle = new Tile[width * height];
			back = new Tile[width * height];
		}

		public string GetValue(string key)
		{
			string output = null;
			this.values.TryGetValue(key, out output);
			return output;
		}

		public void SetValue(string key, string value)
		{
			this.values[key] = value;
		}
		public void SetTile(int column, int row, Tile tile, int front_ness)
		{
			Tile[] layer = back;
			if (front_ness == 0) layer = front;
			if (front_ness == 1) layer = middle;

			if (row >= 0 && row < this.height && column >= 0 && column < this.width)
			{
				layer[row * this.width + column] = tile;
			}
		}

		public void FillTile(int column, int row, Grid front, Grid middle, Grid back)
		{
			if (column < 0 || column >= this.width || row < 0 || row >= this.height)
			{
				return;
			}

			int index = column + row * this.width;
			Image newImage;

			newImage = Tile.GetImageFromTile(this.front[index], column, row);
			front.Children.RemoveAt(index);
			front.Children.Insert(index, newImage);

			newImage = Tile.GetImageFromTile(this.middle[index], column, row);
			middle.Children.RemoveAt(index);
			middle.Children.Insert(index, newImage);

			newImage = Tile.GetImageFromTile(this.back[index], column, row);
			back.Children.RemoveAt(index);
			back.Children.Insert(index, newImage);
		}

		public int Width { get { return this.width; } }
		public int Height { get { return this.height; } }

		public void FillGrids(Grid front, Grid middle, Grid back)
		{
			foreach (Grid grid in new Grid[] { front, middle, back })
			{
				grid.Children.Clear();
				grid.Width = this.width * 16;
				grid.Height = this.height * 16;
			}

			for (int y = 0; y < this.height; ++y)
			{
				for (int x = 0; x < this.width; ++x)
				{
					int index = y * this.width + x;
					Image img = Tile.GetImageFromTile(this.front[index], x, y);
					front.Children.Add(img);
					img = Tile.GetImageFromTile(this.middle[index], x, y);
					middle.Children.Add(img);
					img = Tile.GetImageFromTile(this.back[index], x, y);
					back.Children.Add(img);

				}
			}
		}

		public void Save()
		{
			List<string> tile_ids = new List<string>();
			for (int i = 0; i < this.back.Length; ++i)
			{
				List<string> tile = new List<string>();
				Tile t = this.back[i];
				if (t != null)
				{
					tile.Add(t.Id);
				}

				t = this.middle[i];
				if (t != null)
				{
					tile.Add(t.Id);
				}

				t = this.front[i];
				if (t != null)
				{
					tile.Add(t.Id);
				}

				if (tile.Count == 0)
				{
					tile.Add("0");
				}

				tile_ids.Add(string.Join(",", tile.ToArray()));
			}

			this.values["tiles"] = string.Join(" ", tile_ids.ToArray());
			this.values["width"] = this.width.ToString();

			List<string> output = new List<string>();

			foreach (string key in this.values.Keys)
			{
				if (this.values[key] != null)
				{
					output.Add(key + ":" + this.values[key]);
				}
			}

			if (string.IsNullOrEmpty(this.file))
			{
				System.Windows.Forms.SaveFileDialog dialog = new System.Windows.Forms.SaveFileDialog();
				dialog.InitialDirectory = MainWindow.LevelsDirectory;
				dialog.ShowDialog();
				this.file = dialog.FileName;
			}

			System.IO.File.WriteAllText(this.file, string.Join("\r\n", output.ToArray()));
		}

		public void ResizeTo(int newWidth, int newHeight)
		{
			Tile[] newFront = new Tile[newWidth * newHeight];
			Tile[] newMiddle = new Tile[newWidth * newHeight];
			Tile[] newBack = new Tile[newWidth * newHeight];

			for (int y = 0; y < newHeight; ++y)
			{
				if (y < this.height)
				{
					for (int x = 0; x < newWidth; ++x)
					{
						if (x < this.width)
						{
							int index = y * newWidth + x;
							int oldIndex = y * this.width + x;
							newFront[index] = this.front[oldIndex];
							newMiddle[index] = this.middle[oldIndex];
							newBack[index] = this.back[oldIndex];
						}
					}
				}
			}

			this.front = newFront;
			this.middle = newMiddle;
			this.back = newBack;

			this.width = newWidth;
			this.height = newHeight;
		}

		public List<Door> GetDoors(FrameworkElement artboard)
		{
			List<Door> doors = new List<Door>();
			Tile tile;
			foreach (Tile[] tileLayer in new Tile[][] { front, middle, back })
			{
				for (int i = 0; i < tileLayer.Length; ++i)
				{
					tile = tileLayer[i];
					if (tile != null && tile.IsDoor)
					{
						int y = i / this.width;
						int x = i - y * this.width;

						doors.Add(new Door(artboard, x, y, this.width, this.height) { IsSet = false });
					}
				}
			}

			return doors;
		}

		public Map(string filepath)
		{
			this.file = filepath;
			string[] lines = System.IO.File.ReadAllText(filepath).Trim().Split('\n');

			foreach (string line in lines)
			{
				string[] parts = line.Split(':');
				string key = parts[0].Trim();
				string value = parts[1].TrimStart();
				for (int i = 2; i < parts.Length; ++i)
				{
					value += parts[i];
				}
				value = value.TrimEnd();
				values.Add(key, value);
			}

			int width = int.Parse(values["width"]);
			string[] tile_keys = values["tiles"].Split(' ');
			int height = tile_keys.Length / width;

			this.width = width;
			this.height = height;

			front = new Tile[width * height];
			middle = new Tile[width * height];
			back = new Tile[width * height];

			for (int i = 0; i < tile_keys.Length; ++i)
			{
				string[] tile_ids = tile_keys[i].Split(',');

				if (tile_ids.Length == 1)
				{
					middle[i] = TileLibrary.GetTile(tile_ids[0]);
				}
				else if (tile_ids.Length == 2)
				{
					front[i] = TileLibrary.GetTile(tile_ids[1]);
					middle[i] = TileLibrary.GetTile(tile_ids[0]);
				}
				else if (tile_ids.Length == 3)
				{
					front[i] = TileLibrary.GetTile(tile_ids[2]);
					middle[i] = TileLibrary.GetTile(tile_ids[1]);
					back[i] = TileLibrary.GetTile(tile_ids[0]);
				}
				else
				{
					System.Windows.MessageBox.Show("More than 3 stacked tiles isn't suppored by the map editor. talk to Blake. Don't save this file");
					break;
				}
			}

		}
	}
}
