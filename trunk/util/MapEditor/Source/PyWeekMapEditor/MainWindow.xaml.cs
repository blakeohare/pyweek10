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
			this.ArtBoard_Front.MouseDown += new MouseButtonEventHandler(ArtBoard_Front_MouseDown);
			this.ArtBoard_Front.MouseUp += new MouseButtonEventHandler(ArtBoard_Front_MouseUp);
			this.ArtBoard_Front.MouseMove += new MouseEventHandler(ArtBoard_Front_MouseMove);

			this.visible_back.Checked += new RoutedEventHandler(visible_back_Checked);
			this.visible_back.Unchecked += new RoutedEventHandler(visible_back_Unchecked);
			this.visible_middle.Checked += new RoutedEventHandler(visible_middle_Checked);
			this.visible_middle.Unchecked += new RoutedEventHandler(visible_middle_Unchecked);
			this.visible_front.Checked += new RoutedEventHandler(visible_front_Checked);
			this.visible_front.Unchecked += new RoutedEventHandler(visible_front_Unchecked);
		}

		void visible_front_Unchecked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Front.Visibility = System.Windows.Visibility.Hidden;
		}

		void visible_front_Checked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Front.Visibility = System.Windows.Visibility.Visible;
		}

		void visible_middle_Unchecked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Middle.Visibility = System.Windows.Visibility.Hidden;
		}

		void visible_middle_Checked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Middle.Visibility = System.Windows.Visibility.Visible;
		}

		void visible_back_Unchecked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Back.Visibility = System.Windows.Visibility.Hidden;
		}

		void visible_back_Checked(object sender, RoutedEventArgs e)
		{
			this.ArtBoard_Back.Visibility = System.Windows.Visibility.Visible;
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
				Point p = e.GetPosition(sender as Grid);
				int col = (int)(p.X / 16);
				int row = (int)(p.Y / 16);

				this.activeMap.SetTile(col, row, this.tile_palette.SelectedItem as Tile, this.FrontNess);
				this.activeMap.FillTile(col, row,
					this.ArtBoard_Front,
					this.ArtBoard_Middle,
					this.ArtBoard_Back);
			}
		}

		void ArtBoard_Front_MouseUp(object sender, MouseButtonEventArgs e)
		{
			this.mousedown = false;
		}

		void ArtBoard_Front_MouseDown(object sender, MouseButtonEventArgs e)
		{
			this.mousedown = true;
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
		}

		void file_new_Click(object sender, RoutedEventArgs e)
		{
			
		}
	}
}
