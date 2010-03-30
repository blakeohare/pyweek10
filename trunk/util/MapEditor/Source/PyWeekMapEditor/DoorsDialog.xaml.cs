using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace PyWeekMapEditor
{
	/// <summary>
	/// Interaction logic for DoorsDialog.xaml
	/// </summary>
	public partial class DoorsDialog : Window
	{
		private string originalDoorsValue;
		private string finalDoorsValue;
		private Map map;
		private List<Door> doors = new List<Door>();
		private bool saved = false;

		public DoorsDialog(Map mapdata, FrameworkElement artboard)
		{
			this.originalDoorsValue = mapdata.GetValue("doors") ?? "";
			this.map = mapdata;
			this.InitDoors(artboard);
			
			InitializeComponent();

			this.DoorsList.ItemsSource = this.doors;

			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
		}

		void CancelButton_Click(object sender, RoutedEventArgs e)
		{
			this.saved = false;
			this.Close();
		}

		void SaveButton_Click(object sender, RoutedEventArgs e)
		{
			this.saved = true;
			List<string> values = new List<string>();
			foreach (Door door in this.doors)
			{
				string value =
					door.X.ToString() + "," +
					door.Y.ToString() + "|" +
					door.ToScreen + "," +
					door.ToLocation;

				values.Add(value);
			}

			this.finalDoorsValue = string.Join(" ", values.ToArray());
			this.Close();
		}

		public string FinalStringValue
		{
			get
			{
				if (this.saved)
				{
					return this.finalDoorsValue;
				}
				return this.originalDoorsValue;
			}
		}

		private void InitDoors(FrameworkElement artboard)
		{
			List<Door> doors = this.map.GetDoors(artboard);
			string[] doorData = this.originalDoorsValue.Split(' ');
			if (doorData.Length > 0 && !string.IsNullOrEmpty(doorData[0]))
			{
				foreach (string door in doorData)
				{
					string[] pieces = door.Split('|');
					string[] coords = pieces[0].Split(',');
					string[] dest = pieces[1].Split(',');

					int x = int.Parse(coords[0]);
					int y = int.Parse(coords[1]);
					string screen = dest[0];
					string start_loc = dest[1];

					foreach (Door doorInstance in doors)
					{
						if (doorInstance.X == x && doorInstance.Y == y)
						{
							doorInstance.ToLocation = start_loc;
							doorInstance.ToScreen = screen;
							doorInstance.IsSet = true;
							break;
						}
					}
				}
			}

			this.doors = doors;
		}

		public List<Door> Doors
		{
			get { return this.doors; }
		}
	}

	public class Door
	{
		private ImageSource level_image;
		private double level_height;
		private double level_width;
		public Door(FrameworkElement artboard, int x, int y, int level_width, int level_height)
		{
			this.level_width = level_width;
			this.level_height = level_height;
			this.X = x;
			this.Y = y;
			RenderTargetBitmap bmp = new RenderTargetBitmap((int)artboard.ActualWidth, (int)artboard.ActualHeight, 96, 96, PixelFormats.Pbgra32);
			bmp.Render(artboard);
			this.level_image = bmp;
		}
		public int X { get; private set; }
		public int Y { get; private set; }
		public string ToLocation { get; set; }
		public string ToScreen { get; set; }
		public bool IsSet { get; set; }
		public string Location { get { return "At: (" + this.X.ToString() + ", " + this.Y.ToString() + ")"; } }

		public ImageBrush Thumbnail
		{
			get
			{
				return new ImageBrush(this.level_image)
				{
					Transform = new TransformGroup()
					{
						Children = new TransformCollection()
						{/*
						  * >:( 
						  * I can't get this to work
							new TranslateTransform() { X = 0, Y = 0 },
							new ScaleTransform() { ScaleX = 4, ScaleY = 4 * level_height / level_width },
							*/
						}
					}
				};
			}
		}
	}
}
