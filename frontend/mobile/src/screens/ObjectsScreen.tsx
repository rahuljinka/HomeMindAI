import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Search, Package, MapPin } from 'lucide-react-native';
import apiClient from '../api/client';

interface StoredObject {
  id: number;
  name: string;
  category?: string;
  description?: string;
  current_location?: {
    room: { name: string };
    furniture?: { name: string };
    container?: { name: string };
  };
  updated_at: string;
}

export default function ObjectsScreen() {
  const [objects, setObjects] = useState<StoredObject[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchObjects = async (query = '') => {
    try {
      setLoading(true);
      const endpoint = query ? `/search?q=${query}` : '/objects/';
      const response = await apiClient.get(endpoint);
      setObjects(response.data);
    } catch (error) {
      console.error('Error fetching objects:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchObjects();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchObjects(search);
  };

  const renderObject = ({ item }: { item: StoredObject }) => (
    <TouchableOpacity style={styles.card}>
      <View style={styles.cardHeader}>
        <Package size={20} color="#007AFF" />
        <Text style={styles.objectName}>{item.name}</Text>
        {item.category && <Text style={styles.categoryBadge}>{item.category}</Text>}
      </View>
      
      <View style={styles.locationContainer}>
        <MapPin size={16} color="#666" />
        <Text style={styles.locationText}>
          {[
            item.current_location?.room?.name,
            item.current_location?.furniture?.name,
            item.current_location?.container?.name
          ].filter(Boolean).join(' → ')}
        </Text>
      </View>
      
      <Text style={styles.updatedText}>
        Last updated: {new Date(item.updated_at).toLocaleDateString()}
      </Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Search size={20} color="#999" />
        <TextInput
          style={styles.searchInput}
          placeholder="Search objects..."
          value={search}
          onChangeText={(text) => {
            setSearch(text);
            fetchObjects(text);
          }}
        />
      </View>

      {loading && !refreshing ? (
        <ActivityIndicator style={styles.loader} size="large" color="#007AFF" />
      ) : (
        <FlatList
          data={objects}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderObject}
          contentContainerStyle={styles.list}
          refreshing={refreshing}
          onRefresh={onRefresh}
          ListEmptyComponent={
            <Text style={styles.emptyText}>No objects found. Try asking HomeMind to remember something!</Text>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa' },
  searchContainer: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: '#fff', 
    margin: 15, 
    paddingHorizontal: 15, 
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#eee'
  },
  searchInput: { flex: 1, paddingVertical: 12, marginLeft: 10, fontSize: 16 },
  list: { padding: 15, paddingTop: 0 },
  card: { 
    backgroundColor: '#fff', 
    padding: 15, 
    borderRadius: 12, 
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 5,
    elevation: 2
  },
  cardHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  objectName: { fontSize: 18, fontWeight: '600', marginLeft: 10, flex: 1 },
  categoryBadge: { 
    backgroundColor: '#E3F2FD', 
    color: '#007AFF', 
    paddingHorizontal: 8, 
    paddingVertical: 2, 
    borderRadius: 10, 
    fontSize: 12, 
    overflow: 'hidden' 
  },
  locationContainer: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  locationText: { color: '#444', marginLeft: 5, fontSize: 14 },
  updatedText: { color: '#999', fontSize: 12, textAlign: 'right' },
  loader: { marginTop: 50 },
  emptyText: { textAlign: 'center', marginTop: 50, color: '#999', paddingHorizontal: 40, lineHeight: 20 }
});
