using System;
using System.Windows.Controls;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace PyWeekMapEditor
{
	public class TileLibrary
	{
		private Dictionary<string, Tile> tiles = new Dictionary<string, Tile>();
		private List<string> folders = new List<string>();
		private Dictionary<string, List<Tile>> folder_members = new Dictionary<string, List<Tile>>();

		public static Image GetImage(string id)
		{
			return new Image() { Source = Instance.tiles[id].Source };
		}

		public static Tile GetTile(string id)
		{
			return Instance.tiles[id];
		}

		public TileLibrary()
		{
			string tileDir = MainWindow.TileDirectory;
			string tileImageDir = MainWindow.TileImagesDirectory;

			string[] tile_files = System.IO.Directory.GetFiles(tileDir);
			foreach (string file in tile_files)
			{
				if (file.EndsWith(".txt"))
				{
					string[] lines = System.IO.File.ReadAllText(System.IO.Path.Combine(tileDir, file)).Split('\n');
					foreach (string line in lines)
					{
						string trimmed = line.Trim();
						if (trimmed.Length > 0 && trimmed[0] != '#')
						{
							string[] parts = trimmed.Split('\t');
							try
							{
								string id = parts[0];
								string[] org = parts[1].Split('/');
								string folder = org[0];
								string name = org[1];
								string[] images = parts[2].Split('|');
								Tile t = new Tile(images, id, name, file.EndsWith("\\doors.txt"));
								this.AddTileToHierarchy(t, folder, name);
								this.tiles.Add(id, t);
							}
							catch (Exception e)
							{

							}
						}
					}
				}
			}
			TileSorter ts = new TileSorter();
			this.folders.Sort();
			foreach (string folder in this.folders)
			{
				this.folder_members[folder].Sort(ts);
			}
		}

		public List<string> Folders
		{
			get { return this.folders; }
		}

		public List<Tile> TilesInFolder(string folder)
		{
			return this.folder_members[folder];
		}

		private class TileSorter : IComparer<Tile>
		{
			public int Compare(Tile x, Tile y)
			{
				return x.Name.CompareTo(y.Name);
			}
		}

		private void AddTileToHierarchy(Tile tile, string folder, string name)
		{
			if (!this.folder_members.ContainsKey(folder))
			{
				this.folder_members.Add(folder, new List<Tile>());
				this.folders.Add(folder);
			}

			this.folder_members[folder].Add(tile);
		}


		private static TileLibrary instance = null;
		public static TileLibrary Instance
		{
			get
			{
				if (instance == null)
				{
					instance = new TileLibrary();
				}
				return instance;
			}
		}
	}
}
