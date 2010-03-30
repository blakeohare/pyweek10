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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PyWeekMapEditor
{
	/// <summary>
	/// Interaction logic for MainWindow.xaml
	/// </summary>
	public partial class MainWindow : Window
	{
		private static readonly SavedConfiguration Config = new SavedConfiguration();
		public static readonly string TileDirectory = System.IO.Path.Combine(Config.RootPath, "tiles");
		public static readonly string TileImagesDirectory = System.IO.Path.Combine(Config.RootPath, "images\\tiles");
		public static readonly string ImagesDirectory = System.IO.Path.Combine(Config.RootPath, "images");
		public static readonly string BackgroundsDirectory = System.IO.Path.Combine(ImagesDirectory, "backgrounds");
		public static readonly string LevelsDirectory = System.IO.Path.Combine(Config.RootPath, "levels\\levels");
		public static readonly string User = Config.User;
		public static readonly string Prefix = Config.Prefix;

		private Map activeMap = null;

		public MainWindow()
		{
			InitializeComponent();

			this.InitializeFolders();

			this.file_new.Click += new RoutedEventHandler(file_new_Click);
			this.file_open.Click += new RoutedEventHandler(file_open_Click);
			this.file_save.Click += new RoutedEventHandler(file_save_Click);
			this.maps_edit_doors.Click += new RoutedEventHandler(maps_edit_doors_Click);
			this.maps_starting_locations.Click += new RoutedEventHandler(maps_starting_locations_Click);
			this.map_default_start.Click += new RoutedEventHandler(map_default_start_Click);
			this.map_victory_x.Click += new RoutedEventHandler(map_victory_x_Click);
			this.file_change_size.Click += new RoutedEventHandler(file_change_size_Click);
			this.map_background.Click += new RoutedEventHandler(map_background_Click);

			this.ClickCatcher.MouseDown += new MouseButtonEventHandler(ArtBoard_Front_MouseDown);
			this.ClickCatcher.MouseUp += new MouseButtonEventHandler(ArtBoard_Front_MouseUp);
			this.ClickCatcher.MouseMove += new MouseEventHandler(ArtBoard_Front_MouseMove);

			this.visible_back.Checked += new RoutedEventHandler(visible_back_Checked);
			this.visible_back.Unchecked += new RoutedEventHandler(visible_back_Unchecked);
			this.visible_middle.Checked += new RoutedEventHandler(visible_middle_Checked);
			this.visible_middle.Unchecked += new RoutedEventHandler(visible_middle_Unchecked);
			this.visible_front.Checked += new RoutedEventHandler(visible_front_Checked);
			this.visible_front.Unchecked += new RoutedEventHandler(visible_front_Unchecked);
		}

		void map_background_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				string bg_scroll = this.activeMap.GetValue("background_scroll_rate") ?? "0";
				string bg_image = this.activeMap.GetValue("background_image") ?? "";
				BackgroundDialog dialog = new BackgroundDialog(bg_image, bg_scroll);
				dialog.ShowDialog();
				if (dialog.Saved)
				{
					bg_scroll = dialog.ScrollRate.Trim();
					bg_scroll = bg_scroll == "" ? null : bg_scroll;

					bg_image = dialog.File.Trim();
					bg_image = bg_image == "" ? null : bg_image;

					this.activeMap.SetValue("background_scroll_rate", bg_scroll);
					this.activeMap.SetValue("background_image", bg_image);

					this.RefreshBackground();
				}
			}
		}

		private void RefreshBackground()
		{
			if (this.activeMap != null)
			{
				string bg_image = this.activeMap.GetValue("background_image");
				if (!string.IsNullOrEmpty(bg_image))
				{
					this.BackgroundImageFile.ImageSource = new BitmapImage(new Uri(System.IO.Path.Combine(BackgroundsDirectory, bg_image + ".png")));
				}
				else
				{
					this.BackgroundImageFile.ImageSource = null;
				}
			}
			else
			{
				this.BackgroundImageFile.ImageSource = null;
			}
		}

		void file_change_size_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				NewMapDialog dialog = new NewMapDialog(this.activeMap);
				dialog.ShowDialog();

				this.activeMap.FillGrids(
					this.ArtBoard_Front,
					this.ArtBoard_Middle,
					this.ArtBoard_Back);
			}
		}

		void map_victory_x_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				VictoryXDialog dialog = new VictoryXDialog(this.activeMap.GetValue("victoryX"));
				dialog.ShowDialog();
				if (int.Parse(dialog.FinalValue) != 0)
				{
					this.activeMap.SetValue("victoryX", dialog.FinalValue);
				}
				else
				{
					this.activeMap.SetValue("victoryX", null);
				}
			}
		}

		void map_default_start_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				DefaultLocationDialog dialog = new DefaultLocationDialog(this.activeMap.GetValue("default_start"), this.activeMap.GetValue("start_locations") ?? "");
				dialog.ShowDialog();
				this.activeMap.SetValue("default_start", dialog.FinalValue);
			}
		}

		void maps_starting_locations_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				StartLocationsDialog dialog = new StartLocationsDialog(this.activeMap.GetValue("start_locations"));
				dialog.ShowDialog();
				this.activeMap.SetValue("start_locations", dialog.FinalValue);
			}
		}

		void maps_edit_doors_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				DoorsDialog dialog = new DoorsDialog(this.activeMap, this.Artboard);
				dialog.ShowDialog();
				this.activeMap.SetValue("doors", dialog.FinalStringValue);
			}
		}

		void visible_front_Unchecked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Front.Opacity = 0.2;
		}

		void visible_front_Checked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Front.Opacity = 1.0;
		}

		void visible_middle_Unchecked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Middle.Opacity = 0.2;
		}

		void visible_middle_Checked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Middle.Opacity = 1.0;
		}

		void visible_back_Unchecked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Back.Opacity = 0.2;
		}

		void visible_back_Checked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Back.Opacity = 1.0;
		}

		void file_save_Click(object sender, RoutedEventArgs e)
		{
			if (this.activeMap != null)
			{
				this.activeMap.Save();
			}
		}

		private bool mousedown = false;

		private int FrontNess
		{
			get
			{
				if (this.active_front.IsChecked.HasValue && this.active_front.IsChecked.Value)
				{
					return 0;
				}

				if (this.active_middle.IsChecked.HasValue && this.active_middle.IsChecked.Value)
				{
					return 1;
				}

				return 2;
			}
		}

		void ArtBoard_Front_MouseMove(object sender, MouseEventArgs e)
		{
			if (mousedown && this.activeMap != null)
			{
				this.DoSetting(sender, e);
			}
		}

		private void DoSetting(object sender, MouseEventArgs e)
		{
			Point p = e.GetPosition(this.ArtBoard_Front);
			int col = (int)(p.X / 16);
			int row = (int)(p.Y / 16);

			this.activeMap.SetTile(col, row, this.tile_palette.SelectedItem as Tile, this.FrontNess);
			this.activeMap.FillTile(col, row,
				this.ArtBoard_Front,
				this.ArtBoard_Middle,
				this.ArtBoard_Back);
		}

		void ArtBoard_Front_MouseUp(object sender, MouseButtonEventArgs e)
		{
			this.mousedown = false;
		}

		void ArtBoard_Front_MouseDown(object sender, MouseButtonEventArgs e)
		{
			this.mousedown = true;
			this.DoSetting(sender, e);
		}

		private void InitializeFolders()
		{
			ListBox folders = this.folder_listing;
			folders.ItemsSource = TileLibrary.Instance.Folders;
			folders.SelectionChanged += new SelectionChangedEventHandler(folders_SelectionChanged);
			folders.SelectedIndex = 0;
		}

		void folders_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			ListBox tiles = this.tile_palette;
			List<Tile> tile_list = TileLibrary.Instance.TilesInFolder(this.folder_listing.SelectedItem.ToString());
			tiles.ItemsSource = tile_list;

		}

		void file_open_Click(object sender, RoutedEventArgs e)
		{
			System.Windows.Forms.OpenFileDialog dialog = new System.Windows.Forms.OpenFileDialog();
			dialog.InitialDirectory = LevelsDirectory;
			dialog.ShowDialog();
			string filename = dialog.FileName;

			try
			{
				this.activeMap = new Map(filename);
				this.activeMap.FillGrids(
					this.ArtBoard_Front,
					this.ArtBoard_Middle,
					this.ArtBoard_Back);
			}
			catch (Exception)
			{
				System.Windows.MessageBox.Show("Invalid file");
			}
			this.RefreshBackground();
		}

		void file_new_Click(object sender, RoutedEventArgs e)
		{
			NewMapDialog dialog = new NewMapDialog();
			dialog.ShowDialog();
			if (dialog.OutputMap != null)
			{
				this.activeMap = dialog.OutputMap;

				this.ArtBoard_Back.Children.Clear();
				this.ArtBoard_Middle.Children.Clear();
				this.ArtBoard_Front.Children.Clear();

				this.activeMap.FillGrids(
					this.ArtBoard_Front,
					this.ArtBoard_Middle,
					this.ArtBoard_Back);

				this.RefreshBackground();
			}
		}
	}
}
