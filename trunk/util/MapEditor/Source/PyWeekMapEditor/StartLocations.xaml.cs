using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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
	/// Interaction logic for StartLocations.xaml
	/// </summary>
	public partial class StartLocationsDialog : Window
	{
		private ObservableCollection<StartLocation> StartLocations { get; set; }
		private string originalValue;
		private bool saved = false;
		public StartLocationsDialog(string originalValue)
		{
			this.originalValue = originalValue;
			this.InitLocList();
			this.InitializeComponent();
			this.StartLocationsList.ItemsSource = this.StartLocations;
			this.AddButton.Click += new RoutedEventHandler(AddButton_Click);
			this.CancelButton.Click += new RoutedEventHandler(CancelButton_Click);
			this.SaveButton.Click += new RoutedEventHandler(SaveButton_Click);
		}

		private void InitLocList()
		{
			this.StartLocations = new ObservableCollection<StartLocation>();
			if (!string.IsNullOrEmpty(this.originalValue))
			{
				string[] locs = this.originalValue.Split(' ');
				foreach (string loc in locs)
				{
					string[] bits = loc.Split(',');
					this.StartLocations.Add(new StartLocation(this.StartLocations) { Name = bits[0], X = bits[1], Y = bits[2] });
				}
			}
		}

		void CancelButton_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		void SaveButton_Click(object sender, RoutedEventArgs e)
		{
			this.saved = true;
			this.Close();
		}

		public string FinalValue
		{
			get
			{
				if (this.saved)
				{
					List<string> values = new List<string>();
					foreach (StartLocation loc in this.StartLocations)
					{
						values.Add(loc.Name + "," + loc.X + "," + loc.Y);
					}
					return string.Join(" ", values.ToArray());
				}
				return this.originalValue;
			}
		}

		void AddButton_Click(object sender, RoutedEventArgs e)
		{
			this.StartLocations.Add(new StartLocation(this.StartLocations));
		}

		private class StartLocation
		{
			private ObservableCollection<StartLocation> locationList;

			public StartLocation(ObservableCollection<StartLocation> locationList) {
				this.locationList = locationList;
			}
			public string Name { get; set; }
			public string X { get; set; }
			public string Y { get; set; }

			public ICommand RemoveMe
			{
				get
				{
					return new RemoveCommand(this.locationList, this);
				}
			}
			private class RemoveCommand : ICommand
			{
				private ObservableCollection<StartLocation> locationList;
				private StartLocation location;
				public RemoveCommand(ObservableCollection<StartLocation> locationList, StartLocation location)
				{
					this.location = location;
					this.locationList = locationList;
				}

				public bool CanExecute(object parameter)
				{
					return true;
				}

				public event EventHandler CanExecuteChanged;

				public void Execute(object parameter)
				{
					this.locationList.Remove(this.location);
				}
			}
		}
	}
}
