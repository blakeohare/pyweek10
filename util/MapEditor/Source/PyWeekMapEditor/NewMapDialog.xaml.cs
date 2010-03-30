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
	/// Interaction logic for NewMapDialog.xaml
	/// </summary>
	public partial class NewMapDialog : Window
	{
		public  Map OutputMap { get; private set; }
		private bool resize = false;

		// hijacking this for an easy resize dialog
		public NewMapDialog(Map oldMap)
		{
			this.InitializeComponent();
			this.SaveButton.Content = "Resize";
			this.Title = "Resize";
			this.resize = true;
			this.OutputMap = oldMap;
			this.mapWidth.Text = oldMap.Width.ToString();
			this.mapHeight.Text = oldMap.Height.ToString();
			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
		}

		public NewMapDialog()
		{
			InitializeComponent();
			this.OutputMap = null;
			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
		}

		void CancelButton_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void SaveButton_Click(object sender, RoutedEventArgs e)
		{
			int width = int.Parse(this.mapWidth.Text);
			int height = int.Parse(this.mapHeight.Text);

			if (this.resize)
			{
				this.OutputMap.ResizeTo(width, height);
			}
			else
			{
				this.OutputMap = new Map(width, height);
			}
			this.Close();
		}
	}
}
